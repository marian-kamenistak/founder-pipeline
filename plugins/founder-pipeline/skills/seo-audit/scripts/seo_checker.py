#!/usr/bin/env python3
"""
seo_checker.py — deterministic on-page auditor for /founder-pipeline:seo-audit

Usage:
  python3 seo_checker.py --url https://example.com/page --json
  python3 seo_checker.py --file page.html --json
  python3 seo_checker.py --url https://example.com/page --keyword "engineering leadership coach"
  python3 seo_checker.py                       # demo mode with embedded sample HTML

Output shape (stable — /founder-pipeline:seo-audit and any future caller reads this):

  {
    "overall": 0-100,          # renormalised over MEASURED layers only
    "coverage": 0-100,         # share of check weight that was actually measurable
    "confidence": "high|medium|low",
    "layers":  { "indexability": {...}, "on_page": {...},
                 "extractability": {...}, "delivery": {...} },
    "checks":  { "<id>": {...} },
    "gate":    { "pass": bool, "blockers": [ ... ] }
  }

Design rules, do not break them:
  * An unmeasured check is NEVER a zero. It leaves both numerator and denominator.
  * Schema is REPORTED, never scored. Presence of JSON-LD earns no points.
  * Word count is REPORTED, never scored. It survives only as a thin-content gate floor.
  * The Launch Gate is binary and separate. It is never traded against a high score.
"""

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

TIMEOUT = 15

UA_GPTBOT = ("Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); "
             "compatible; GPTBot/1.2; +https://openai.com/gptbot")
UA_GOOGLEBOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
UA_DEFAULT = "Mozilla/5.0 (compatible; seo-audit/2.0)"

# Patterns that mean "this page server-rendered a placeholder and expected JS to
# replace it". AI crawlers execute zero JavaScript, so a placeholder IS the page.
# Matched against the SCRIPT-STRIPPED body only, and anchored, because bare
# substrings like "nan" hit "finance"/"maintenance" and produce confident nonsense.
PLACEHOLDER_PATTERNS = [
    re.compile(r"(?<![\w-])(loading\s*(?:\.\.\.|…))", re.I),
    re.compile(r"(?<![\w-])(na[čc][íi]t[áa]n[íi]\s*(?:\.\.\.|…)?)", re.I),
    re.compile(r"(enable javascript|javascript is required|requires javascript)", re.I),
    re.compile(r"\{\{\s*[\w.$]+\s*\}\}"),          # unrendered template braces
    re.compile(r"(?<![\w-])(undefined|NaN)(?![\w-])"),
]

SCRIPT_STYLE_RE = re.compile(r"<(script|style|template|noscript)\b[^>]*>.*?</\1>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def visible_text(html):
    """Rough visible-text view: drop script/style/template/noscript, then tags."""
    return TAG_RE.sub(" ", SCRIPT_STYLE_RE.sub(" ", html or ""))


# ---------------------------------------------------------------------------
# HTML parsing
# ---------------------------------------------------------------------------

class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta_description = ""
        self.robots_meta = ""
        self.canonical = ""
        self.h_tags = []            # [(level, text)]
        self._current_h = None
        self._current_h_text = []
        self.images = []            # [{"src", "alt"}]
        self.links = []             # [{"href", "text"}]
        self._current_link_text = []
        self._current_link_href = ""
        self._in_link = False
        self.body_text_parts = []
        self._in_body = False
        self._in_script = False
        self._in_style = False
        self.viewport_meta = False
        self.jsonld_blobs = []
        self._in_jsonld = False
        self._jsonld_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        tag = tag.lower()

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            prop = a.get("property", "").lower()
            content = a.get("content", "")
            if name == "description":
                self.meta_description = content
            elif name == "viewport":
                self.viewport_meta = True
            elif name in ("robots", "googlebot"):
                self.robots_meta = (self.robots_meta + " " + content).strip()
            if prop == "og:description" and not self.meta_description:
                self.meta_description = content
        elif tag == "link":
            if a.get("rel", "").lower() == "canonical":
                self.canonical = a.get("href", "")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._current_h = int(tag[1])
            self._current_h_text = []
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt", None)})
        elif tag == "a":
            self._in_link = True
            self._current_link_href = a.get("href", "")
            self._current_link_text = []
        elif tag == "body":
            self._in_body = True
        elif tag == "script":
            if a.get("type", "").lower() == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = []
            self._in_script = True
        elif tag == "style":
            self._in_style = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self._current_h is not None:
                self.h_tags.append((self._current_h, " ".join(self._current_h_text).strip()))
            self._current_h = None
            self._current_h_text = []
        elif tag == "a":
            if self._in_link:
                self.links.append({
                    "href": self._current_link_href,
                    "text": " ".join(self._current_link_text).strip(),
                })
            self._in_link = False
            self._current_link_text = []
            self._current_link_href = ""
        elif tag == "script":
            if self._in_jsonld:
                self.jsonld_blobs.append("".join(self._jsonld_buf))
                self._in_jsonld = False
                self._jsonld_buf = []
            self._in_script = False
        elif tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self._in_title:
            self.title += data
        if self._current_h is not None:
            self._current_h_text.append(data)
        if self._in_link:
            self._current_link_text.append(data)
        if self._in_body and not self._in_script and not self._in_style:
            self.body_text_parts.append(data)


# ---------------------------------------------------------------------------
# Check plumbing
# ---------------------------------------------------------------------------

# id -> (layer, weight). Weight is *within* the layer.
CHECK_MAP = {
    # Indexability — can a search engine or an AI crawler get it and keep it?
    "canonical":        ("indexability", 30),
    "noindex":          ("indexability", 35),
    "crawler_fetch":    ("indexability", 35),
    # On-page — is the page's own metadata doing its job?
    "title":            ("on_page", 30),
    "meta_description": ("on_page", 20),
    "h1":               ("on_page", 25),
    "heading_hierarchy": ("on_page", 15),
    "internal_links":   ("on_page", 10),
    # Extractability — can an answer be lifted off it without JS and without markup?
    "visible_date":     ("extractability", 25),
    "price_number":     ("extractability", 25),
    "schema_only_faq":  ("extractability", 30),
    "md_twin":          ("extractability", 20),
    # Delivery — how it is served.
    "https":            ("delivery", 35),
    "viewport_meta":    ("delivery", 35),
    "image_alt_text":   ("delivery", 30),
}

LAYER_WEIGHTS = {
    "indexability": 30,
    "on_page": 25,
    "extractability": 25,
    "delivery": 20,
}

# Reported, never scored.
REPORT_ONLY = {"word_count", "schema_types_present"}


def chk(status, note, **extra):
    """status: 'pass' | 'fail' | 'warn' | 'unmeasured' | 'report'."""
    out = {"status": status, "note": note}
    if status == "pass":
        out["score"] = 100
    elif status == "warn":
        out["score"] = 50
    elif status == "fail":
        out["score"] = 0
    else:
        out["score"] = None
    out.update(extra)
    return out


# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------

def _fetch(url, ua=UA_DEFAULT, method="GET"):
    """Return (status, body, error). Never raises."""
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,text/markdown,*/*",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8", errors="replace") if method == "GET" else ""
            return resp.status, body, None
    except urllib.error.HTTPError as e:
        return e.code, "", None
    except ssl.SSLCertVerificationError as e:
        # Do not silently degrade. Some Python builds (notably the python.org macOS
        # framework builds) ship no CA bundle until their certificate installer is run,
        # and then every https fetch fails here. Surface it rather than skipping verification.
        return None, "", f"TLS verification failed ({e}). Run the Python cert installer."
    except Exception as e:  # noqa: BLE001 — surfaced, not swallowed
        return None, "", str(e)


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

# `visible_date` has to work in the language the page is written in, not just English.
# One non-English locale ships as a worked example (Czech, genitive month forms, with and
# without diacritics). Add your own market's month names and date order here — the check
# reports "unmeasured" rather than "fail" for a form it does not recognise, so a missing
# locale reads as a coverage gap, never as a defect on the page.
LOCALE_MONTHS = ("ledna|února|unora|března|brezna|dubna|května|kvetna|června|cervna|"
                 "července|cervence|srpna|září|zari|října|rijna|listopadu|prosince")

DATE_PATTERNS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                                  # 2026-08-22
    re.compile(r"\b\d{1,2}\.\s?\d{1,2}\.\s?\d{4}\b"),                      # 22. 8. 2026 (day-first)
    re.compile(r"\b\d{1,2}\.\s?(" + LOCALE_MONTHS + r")\s+\d{4}\b", re.I),  # 22. srpna 2026
    re.compile(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b", re.I),
    re.compile(r"\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}\b", re.I),
]

PRICE_PATTERN = re.compile(
    r"(?:(?:€|\$|£|Kč|CZK|EUR|USD|GBP|PLN|zł)\s?\d[\d\s.,]*)"
    r"|(?:\d[\d\s.,]*\s?(?:€|\$|£|Kč|CZK|EUR|USD|GBP|PLN|zł))",
    re.I,
)


def _norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _parse_jsonld(blobs):
    types, nodes = [], []
    for blob in blobs:
        try:
            data = json.loads(blob)
        except (ValueError, TypeError):
            types.append("__INVALID_JSON__")
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, dict):
                nodes.append(node)
                t = node.get("@type")
                if isinstance(t, str):
                    types.append(t)
                elif isinstance(t, list):
                    types.extend(x for x in t if isinstance(x, str))
                for v in node.values():
                    if isinstance(v, (list, dict)):
                        stack.append(v)
    return types, nodes


def analyze_html(html, url=None, keyword=None, live=True):
    p = SEOParser()
    p.feed(html)

    body_text = _norm(" ".join(p.body_text_parts))
    body_lower = body_text.lower()
    words = re.findall(r"\b[\w'’-]+\b", body_text, re.UNICODE)
    word_count = len(words)

    parsed_url = urllib.parse.urlparse(url) if url else None
    host = parsed_url.netloc.lower() if parsed_url else ""

    c = {}

    # --- Indexability -------------------------------------------------------
    if p.canonical:
        canon = urllib.parse.urlparse(p.canonical)
        if canon.scheme and canon.netloc:
            same_host = (not host) or canon.netloc.lower().replace("www.", "") == host.replace("www.", "")
            c["canonical"] = (chk("pass", f"Absolute canonical → {p.canonical}", value=p.canonical)
                              if same_host else
                              chk("fail", f"Canonical points off-host → {p.canonical}", value=p.canonical))
        else:
            c["canonical"] = chk("warn", f"Relative canonical ({p.canonical}) — emit an absolute URL",
                                 value=p.canonical)
    else:
        c["canonical"] = chk("fail", "No rel=canonical — duplicate URLs will split signals", value=None)

    robots = p.robots_meta.lower()
    if "noindex" in robots:
        c["noindex"] = chk("fail", f"noindex present in the served HTML (robots: {_norm(p.robots_meta)})",
                           value=_norm(p.robots_meta))
    elif robots:
        c["noindex"] = chk("pass", f"Indexable (robots: {_norm(p.robots_meta)})", value=_norm(p.robots_meta))
    else:
        c["noindex"] = chk("pass", "No robots meta — indexable by default", value=None)

    if live and url:
        agents = {"GPTBot": UA_GPTBOT, "Googlebot": UA_GOOGLEBOT}
        results, problems = {}, []
        for name, ua in agents.items():
            status, body, err = _fetch(url, ua=ua)
            hit = None
            if body:
                vis = visible_text(body[:400000])
                for pat in PLACEHOLDER_PATTERNS:
                    m = pat.search(vis)
                    if m:
                        hit = _norm(m.group(0))[:40]
                        break
            results[name] = {"status": status, "error": err, "placeholder": hit}
            if err:
                problems.append(f"{name}: {err}")
            elif status != 200:
                problems.append(f"{name}: HTTP {status}")
            elif hit:
                problems.append(f"{name}: served placeholder text {hit!r} — AI crawlers run zero JS")
        if any(r["status"] is None and r["error"] for r in results.values()):
            c["crawler_fetch"] = chk("unmeasured", "; ".join(problems), agents=results)
        elif problems:
            c["crawler_fetch"] = chk("fail", "; ".join(problems), agents=results)
        else:
            c["crawler_fetch"] = chk("pass", "200 and real content as GPTBot and Googlebot", agents=results)
    else:
        c["crawler_fetch"] = chk("unmeasured", "No URL — crawler delivery cannot be tested from a file")

    # --- On-page ------------------------------------------------------------
    title = _norm(p.title)
    tl = len(title)
    if not title:
        c["title"] = chk("fail", "Missing title tag", value="", length=0, band="50-60 chars")
    elif 50 <= tl <= 60:
        c["title"] = chk("pass", "Good length", value=title, length=tl, band="50-60 chars")
    elif 40 <= tl <= 70:
        c["title"] = chk("warn", f"{tl} chars — outside 50-60, still usually rendered whole",
                         value=title, length=tl, band="50-60 chars")
    else:
        c["title"] = chk("fail", f"{tl} chars — Google rewrites almost every title above 70",
                         value=title, length=tl, band="50-60 chars")

    desc = _norm(p.meta_description)
    dl = len(desc)
    if not desc:
        c["meta_description"] = chk("fail", "Missing meta description", value="", length=0, band="120-155 chars")
    elif 120 <= dl <= 155:
        c["meta_description"] = chk("pass", "Good length", value=desc[:80], length=dl, band="120-155 chars")
    elif 100 <= dl < 120 or 155 < dl <= 170:
        c["meta_description"] = chk("warn", f"{dl} chars — target 120-155", value=desc[:80], length=dl,
                                    band="120-155 chars")
    else:
        c["meta_description"] = chk("fail", f"{dl} chars — target 120-155", value=desc[:80], length=dl,
                                    band="120-155 chars")

    h1s = [t for lvl, t in p.h_tags if lvl == 1]
    if len(h1s) == 1:
        c["h1"] = chk("pass", "Exactly one H1", count=1, values=h1s)
    elif len(h1s) > 1:
        c["h1"] = chk("fail", f"{len(h1s)} H1s — exactly one", count=len(h1s), values=h1s)
    else:
        c["h1"] = chk("fail", "No H1", count=0, values=[])

    issues, prev = [], 0
    for lvl, text in p.h_tags:
        if prev and lvl > prev + 1:
            issues.append(f"H{prev} → H{lvl} skips a level")
        if not text.strip():
            issues.append(f"Empty H{lvl}")
        prev = lvl
    c["heading_hierarchy"] = (chk("pass", "Hierarchy clean", issues=[], headings=len(p.h_tags))
                              if not issues else
                              chk("warn" if len(issues) <= 2 else "fail",
                                  f"{len(issues)} hierarchy issue(s)", issues=issues[:8],
                                  headings=len(p.h_tags)))

    def _internal(href):
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return False
        u = urllib.parse.urlparse(href)
        if not u.netloc:
            return True
        return bool(host) and u.netloc.lower().replace("www.", "") == host.replace("www.", "")

    internal = [l for l in p.links if _internal(l["href"])]
    external = [l for l in p.links if l["href"].startswith(("http://", "https://")) and not _internal(l["href"])]
    n_int = len(internal)
    c["internal_links"] = (chk("pass", f"{n_int} internal links out", internal=n_int, external=len(external))
                           if n_int >= 3 else
                           chk("fail", f"Only {n_int} internal links out — a revenue page needs 3+",
                               internal=n_int, external=len(external)))
    c["internal_links"]["outbound_note"] = ("Outbound links to named sources are a positive signal, "
                                            "not a leak — they are never penalised here.")

    # --- Extractability -----------------------------------------------------
    head_slice = body_text[:4000]
    dates = [m.group(0) for pat in DATE_PATTERNS for m in pat.finditer(head_slice)]
    c["visible_date"] = (chk("pass", f"Visible date in body text ({dates[0]})", found=dates[:3])
                         if dates else
                         chk("fail", "No human-visible date in the body — recency is unverifiable "
                                     "to a reader and to an AI crawler", found=[]))

    prices = [_norm(m.group(0)) for m in PRICE_PATTERN.finditer(body_text)]
    c["price_number"] = (chk("pass", f"Price answered on the page ({prices[0]})", found=prices[:3])
                         if prices else
                         chk("warn", "No price or figure in visible text — on a transactional page "
                                     "this is the single most-asked question left unanswered", found=[]))

    types, nodes = _parse_jsonld(p.jsonld_blobs)
    invalid = types.count("__INVALID_JSON__")
    clean_types = sorted({t for t in types if t != "__INVALID_JSON__"})
    schema_note = (f"{len(clean_types)} type(s): {', '.join(clean_types)}"
                   if clean_types else "No JSON-LD found")
    if invalid:
        schema_note += f" · {invalid} block(s) failed JSON.parse"
    c["schema_types_present"] = chk("report", schema_note, types=clean_types, invalid_blocks=invalid)

    faq_qs = []
    for node in nodes:
        if node.get("@type") == "Question" or (isinstance(node.get("@type"), list)
                                               and "Question" in node["@type"]):
            ans = node.get("acceptedAnswer") or {}
            if isinstance(ans, list):
                ans = ans[0] if ans else {}
            text = ans.get("text", "") if isinstance(ans, dict) else ""
            faq_qs.append({"q": node.get("name", ""), "a": _norm(re.sub(r"<[^>]+>", " ", text))})

    if not faq_qs:
        c["schema_only_faq"] = chk("unmeasured", "No FAQPage/Question JSON-LD on this page")
    else:
        ghosts = []
        for qa in faq_qs:
            probe = " ".join(qa["a"].split()[:8]).lower()
            if probe and probe not in body_lower:
                ghosts.append(qa["q"][:70])
        if ghosts:
            c["schema_only_faq"] = chk(
                "fail",
                f"{len(ghosts)} of {len(faq_qs)} FAQ answers exist ONLY in markup, not in the visible DOM. "
                "The missing thing is the accordion, not the schema — a fact that lives only in JSON-LD "
                "is retrieved by zero AI platforms.",
                ghost_questions=ghosts[:5], total=len(faq_qs))
        else:
            c["schema_only_faq"] = chk("pass", f"All {len(faq_qs)} FAQ answers also appear in visible text",
                                       total=len(faq_qs))

    if live and url:
        base = urllib.parse.urlsplit(url)
        path = base.path.rstrip("/")
        md_url = urllib.parse.urlunsplit(
            (base.scheme, base.netloc, (path + ".md") if path else "/index.md", "", ""))
        status, body, err = _fetch(md_url)
        if err:
            c["md_twin"] = chk("unmeasured", f"Could not test {md_url}: {err}")
        elif status == 200 and body.strip() and "<html" not in body[:400].lower():
            c["md_twin"] = chk("pass", f"Markdown twin served at {md_url}", url=md_url)
        else:
            c["md_twin"] = chk("warn", f"No markdown twin at {md_url} (HTTP {status}) — optional, "
                                       "cheap, and useful to agents reading the page", url=md_url)
    else:
        c["md_twin"] = chk("unmeasured", "No URL — markdown twin cannot be tested from a file")

    # --- Delivery -----------------------------------------------------------
    if parsed_url:
        c["https"] = (chk("pass", "Served over HTTPS") if parsed_url.scheme == "https"
                      else chk("fail", f"Served over {parsed_url.scheme} — not HTTPS"))
    else:
        c["https"] = chk("unmeasured", "No URL — transport cannot be tested from a file")

    c["viewport_meta"] = (chk("pass", "Mobile viewport tag present") if p.viewport_meta
                          else chk("fail", "Missing viewport meta tag"))

    total_imgs = len(p.images)
    with_alt = sum(1 for i in p.images if i["alt"] is not None and i["alt"].strip())
    if total_imgs == 0:
        c["image_alt_text"] = chk("unmeasured", "No images on the page", total=0)
    else:
        pct = round(with_alt / total_imgs * 100, 1)
        c["image_alt_text"] = (chk("pass", "All images carry alt text", total=total_imgs,
                                   with_alt=with_alt, coverage_pct=pct)
                               if with_alt == total_imgs else
                               chk("warn" if pct >= 80 else "fail",
                                   f"{total_imgs - with_alt} of {total_imgs} images missing alt",
                                   total=total_imgs, with_alt=with_alt, coverage_pct=pct))

    # --- Reported, never scored --------------------------------------------
    c["word_count"] = chk("report",
                          f"{word_count} words. Context only — there is no word-count target. "
                          f"The only threshold that survives is the 150-word thin-content gate floor.",
                          count=word_count)

    # --- Keyword placement (gate input, only when --keyword given) ----------
    if keyword:
        kw = keyword.lower().strip()
        first100 = " ".join(words[:100]).lower()
        slug = (parsed_url.path if parsed_url else "").lower()
        placement = {
            "title": kw in title.lower(),
            "h1": any(kw in h.lower() for h in h1s),
            "url": kw.replace(" ", "-") in slug or kw.replace(" ", "") in slug.replace("-", ""),
            "first_100_words": kw in first100,
        }
        missing = [k for k, v in placement.items() if not v]
        c["keyword_placement"] = (chk("report", f"'{keyword}' present in title, H1, URL and first 100 words",
                                      placement=placement, missing=[])
                                  if not missing else
                                  chk("report", f"'{keyword}' missing from: {', '.join(missing)}",
                                      placement=placement, missing=missing))

    return c, {"word_count": word_count, "h1s": h1s, "title": title, "desc": desc,
               "internal_links": n_int, "keyword": keyword}


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score(checks):
    layers = {}
    for layer, weight in LAYER_WEIGHTS.items():
        ids = [i for i, (l, _) in CHECK_MAP.items() if l == layer]
        measured = [i for i in ids if i in checks and checks[i].get("score") is not None]
        unmeasured = [i for i in ids if i not in measured]
        if measured:
            num = sum(checks[i]["score"] * CHECK_MAP[i][1] for i in measured)
            den = sum(CHECK_MAP[i][1] for i in measured)
            layers[layer] = {
                "score": round(num / den),
                "weight": weight,
                "measured": sorted(measured),
                "unmeasured": sorted(unmeasured),
                "failing": sorted(i for i in measured if checks[i]["status"] == "fail"),
            }
        else:
            layers[layer] = {"score": None, "weight": weight, "measured": [],
                             "unmeasured": sorted(unmeasured), "failing": []}

    scored = {k: v for k, v in layers.items() if v["score"] is not None}
    if scored:
        num = sum(v["score"] * v["weight"] for v in scored.values())
        den = sum(v["weight"] for v in scored.values())
        overall = round(num / den)
    else:
        overall = None

    total_w = sum(w for _, w in CHECK_MAP.values())
    got_w = sum(CHECK_MAP[i][1] for i in CHECK_MAP
                if i in checks and checks[i].get("score") is not None)
    coverage = round(got_w / total_w * 100)
    confidence = "high" if coverage >= 85 else ("medium" if coverage >= 60 else "low")
    return overall, coverage, confidence, layers


def launch_gate(checks, facts):
    """Binary. Never traded against the score."""
    blockers = []
    if checks["noindex"]["status"] == "fail":
        blockers.append("noindex in the served HTML")
    if checks["canonical"]["status"] == "fail":
        blockers.append(checks["canonical"]["note"])
    if checks["h1"]["status"] == "fail":
        blockers.append(checks["h1"]["note"])
    if not facts["title"]:
        blockers.append("No title tag")
    if not facts["desc"]:
        blockers.append("No meta description")
    if checks["https"]["status"] == "fail":
        blockers.append("Not served over HTTPS")
    if checks["crawler_fetch"]["status"] == "fail":
        blockers.append(f"Crawler delivery: {checks['crawler_fetch']['note']}")
    if facts["word_count"] < 150:
        blockers.append(f"Thin page — {facts['word_count']} words (floor is 150)")
    if checks["internal_links"]["status"] == "fail":
        blockers.append(checks["internal_links"]["note"])
    kp = checks.get("keyword_placement")
    if kp and kp.get("missing"):
        blockers.append(f"Primary keyword missing from: {', '.join(kp['missing'])}")
    return {"pass": not blockers, "blockers": blockers}


# ---------------------------------------------------------------------------
# Demo HTML
# ---------------------------------------------------------------------------

DEMO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Engineering Leadership Coaching for First-Time VPs</title>
  <meta name="description" content="One-to-one coaching for first-time engineering VPs and directors. Ninety minutes a fortnight, from EUR 450 a month. Book an intro call.">
  <link rel="canonical" href="https://example.com/coaching">
</head>
<body>
  <h1>Engineering Leadership Coaching for First-Time VPs</h1>
  <p>Updated 22. srpna 2026. Coaching is a fortnightly ninety-minute session for engineers
     who just took their first VP or director role. From EUR 450 per month.</p>
  <h2>What does it cost?</h2>
  <p>EUR 450 per month, billed quarterly. No minimum term beyond the first quarter.</p>
  <h2>Who is it for?</h2>
  <p>Engineers promoted into their first people-leadership role in the last twelve months.</p>
  <a href="/about">About</a>
  <a href="/testimonials">Testimonials</a>
  <a href="/contact">Book an intro call</a>
  <a href="https://hbr.org">Harvard Business Review</a>
  <img src="/coach.jpg" alt="A coach working with a leadership team">
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Deterministic on-page auditor for /founder-pipeline:seo-audit.")
    ap.add_argument("--file", help="Path to an HTML file")
    ap.add_argument("--url", help="URL to fetch and analyze")
    ap.add_argument("--keyword", help="Primary keyword — enables the gate's placement check")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON (what /founder-pipeline:seo-audit reads)")
    args = ap.parse_args()

    url, live = args.url, bool(args.url)
    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        live = False
    elif args.url:
        status, html, err = _fetch(args.url)
        if err or status != 200 or not html:
            print(json.dumps({"error": err or f"HTTP {status}", "url": args.url})
                  if args.json else f"Could not fetch {args.url}: {err or f'HTTP {status}'}")
            sys.exit(2)
    else:
        html, url, live = DEMO_HTML, "https://example.com/coaching", False
        if not args.json:
            print("No input provided — demo mode (network checks report unmeasured).\n")

    checks, facts = analyze_html(html, url=url, keyword=args.keyword, live=live)
    overall, coverage, confidence, layers = score(checks)
    gate = launch_gate(checks, facts)

    out = {"url": url, "overall": overall, "coverage": coverage, "confidence": confidence,
           "layers": layers, "checks": checks, "gate": gate}

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    ICON = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "unmeasured": "----", "report": "info"}
    print("=" * 74)
    print(f"  {url or 'local file'}")
    print(f"  OVERALL {overall}/100   coverage {coverage}%   confidence {confidence}")
    print("=" * 74)
    for layer, w in LAYER_WEIGHTS.items():
        L = layers[layer]
        s = f"{L['score']}/100" if L["score"] is not None else "unmeasured"
        flag = "  <-- below 70, ships with a fix" if (L["score"] is not None and L["score"] < 70) else ""
        print(f"\n  {layer.upper():<16} weight {w:>3}   {s}{flag}")
        for cid in sorted(i for i, (l, _) in CHECK_MAP.items() if l == layer):
            r = checks.get(cid)
            if r:
                print(f"     {ICON[r['status']]:<5} {cid:<20} {r['note'][:90]}")
    print("\n  REPORTED, NEVER SCORED")
    for cid in sorted(REPORT_ONLY | {"keyword_placement"}):
        if cid in checks:
            print(f"     info  {cid:<20} {checks[cid]['note'][:90]}")
    print("\n" + "=" * 74)
    print(f"  LAUNCH GATE: {'PASS' if gate['pass'] else 'FAIL'}   (binary — never traded against the score)")
    for b in gate["blockers"]:
        print(f"     BLOCKER  {b}")
    print("=" * 74)


if __name__ == "__main__":
    main()
