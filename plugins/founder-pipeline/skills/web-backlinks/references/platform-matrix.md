# Platform Matrix — Phase 2 family briefs

Each Phase 2 research subagent gets ONE family section, the brand class, property context (resolved paths), the exclusion list (sent/in-flight, parked, dead from Migrated state — never re-propose these), and this return contract:

- Families 2-6: table `target | contact route | effort S/M/L | impact H/M/L (+DR if known) | cost | risk | evidence URL`, then a 3-line "best first move".
- Family 1: design doc (niche, listing schema, mechanics, seed list, invite template) — no table.
- Verify contact routes on the live site; internal spreadsheets (speaker/member lists) are permitted sources but their emails must be confirmed against the CFP or mail thread of origin, flagged for the orchestrator's suppression pass.
- Anything requiring the owner's account, identity, payment, or a decision → tag OWNER-ONLY / DECISION. Anything requiring an asset/page that doesn't exist → tag BUILD + name the asset.
- Tools: Read, WebSearch, WebFetch or `/founder-pipeline:firecrawl-scrape`. NO paid rank-data calls — ask the orchestrator.

## Brand-class weighting (orchestrator sets; agents honor)

| Brand class | Go-deep families | Notes |
|---|---|---|
| Community | 6 (member badges), 5 (survey), 7 (org entity) | A named membership base is the fuel for both plays |
| Conference | 3 (event listings), 6 (speaker badges), 2 (media partners) | Event listings are the highest-volume easy wins |
| Personal brand | 7 (Wikidata/panel), 1 (directory), 4 (PR/podcasts), 3 (practitioner directories) | Entity work first — it's the base press and any later encyclopaedia coverage build on |
| Marketplace/SaaS | 5 (tools/data), 4 (reviews/PR) | Skip family 7 |

## 1. Directory play (link magnet on your own domain)

Design, don't build (build → `/founder-pipeline:web-site-creator` as a BUILD block). Deliver:
- **Niche** — narrow enough to be THE list: a region-scoped list of practitioners, of events in your category, or of peer communities. Listing competitors deliberately is what makes it credible and linkable.
- **Listing schema** — name, photo/logo, domain, specialty, territory, languages, contact.
- **Inclusion mechanics (Law 4 compliant)** — listing is free via submission form; "verified" = identity confirmation (they respond from their domain), NEVER conditional on a link. The invite may *offer*: "if you find the directory useful, a link is welcome — entirely optional." Referral swap (you pass out-of-territory inquiries, they reciprocate) is a business arrangement offered on its own merits, decoupled from any link ask in the same email.
- **Seed list** — 15-25 peers from `competitors/` + gap data, minus exclusions, each with verified contact route.
- **Invite email template** — benefit first (listing + referrals), optional-link sentence, identification + opt-out line.
- Own domains never appear in each other's directories (portfolio rule).

## 2. Partners & exchanges

Sources: `competitors/INDEX.md`, gap intersection (domains linking to 2+ competitors, not you), adjacent non-competitors (recruiters, VC talent partners, agencies, tool vendors), event media partners (if a partner list exists for the property; else request it from the owner — don't guess).
- **One-way plays first**: guest post where they link you (you don't link back), podcast guesting, newsletter mention swaps (fine to swap — but newsletter web archives ARE crawled, so archived swap links follow the Law 4 nofollow rule).
- Reciprocal site links only within Law 4: max 5 live arrangements per domain, nofollow both directions if agreed as a swap, never three-way (A→B→C→A is a link network), never a partners page built for reciprocation.
- One concrete offer per pitch. Never "let's explore synergies".

## 3. Platform placements

- **Event listings (conference properties — do FIRST)**: open conference-data repos that accept a GitHub PR, developer-event calendars, CFP aggregators, local tech calendars and meetup ecosystems. Free, fast, conference-native.
- **GitHub awesome-lists**: the awesome-list for your discipline, your role, your event category, your format. Draft the PR content; SUBMITTING the PR is OWNER-ONLY (their GitHub identity). Read CONTRIBUTING first; one-line honest description.
- **Speaker databases**: speaker-profile platforms (OWNER-ONLY signup), past-event speaker pages — audit that each links the current domain (fix requests are family 4).
- **Practitioner directories**: the coaching/mentoring/consulting marketplaces for your discipline, plus agency-rating sites for a services property. Any marketplace profile strong enough to outrank the owner's own site for their own name is a DECISION, not an executor block.
- **Local business-networking orgs**: a city or regional business club that publishes a member or speaker list — pursue a member/speaker listing for the audience, not a link swap.
- **Podcast directories**: guest profiles on podcast databases; back-catalog show-notes audit → fix requests.
- **Q&A/community (value-play only)**: Quora, Reddit, HN and the subreddits for your discipline. Executors RESEARCH and DRAFT; posting is OWNER-ONLY (their identity, their karma). Expect nofollow; value = referral traffic + AI-citation surface.
- **Republishing**: dev.to / Medium / Hashnode with canonical URL, author-bio link.

## 4. Digital PR & citations

- **Unlinked mentions (do FIRST — fastest wins)**: the orchestrator runs a content-mention search for the person's name, the organisation's name and the event's name (plus free web search) and passes results in. Every unlinked or wrong-target mention — including mentions pointing at an old or retired domain of yours — gets a one-line fix request. Law 2 carve-out applies: an accurate page is the benefit.
- **Journalist pipelines**: the source-request services (free and paid tiers exist) — ALL are OWNER-ONLY signups; the executor drafts answers to queries the owner forwards. Journalist contacts get the 90-day cross-property cooldown.
- **Regional media pitches**: the tech/business outlets in your home market — expert commentary. Non-primary-language templates are compiled at Phase 3, formal register. Real numbers only, verified against your numbers source of truth at compile time; **never trust a number carried in this file or any other reference doc.**
- **PR wire**: your national news agency's press-release wire, if it has one — free/paid release distribution; treat as PR/citation + AI-search surface, not link value (wire links are nofollow).
- **Broken-link building**: dead competitor pages (a competitor that has shut down is a goldmine) → pull the pages linking to them via the orchestrator's backlink API → "that link is dead, here's a live resource".
- **Podcast guesting**: the two or three big shows in your discipline plus the ones in your home-market language. Show notes = DR 50-80 links. 90-day host cooldown.

**Worked example — a non-Google home market.** The families above assume Google. In markets with a strong domestic search engine and a domestic press ecosystem, the same family produces a different target list: a national search engine's own business catalog, a national news-agency wire, and the two or three domestic tech-business outlets. Treat this as one worked example of what "regional media" means, not as a target list to copy — run the discovery for your own home market.

## 5. Linkbait assets (highest ceiling, slowest fuse)

- **Original data**: an annual "State of X" survey run against your own audience — a dataset nobody else has. 15-40 passive links/cycle from journalists and newsletters. Yearly; time it to whatever quarter your category's planning cycle falls in.
- **Citation-engineered stat pages**: stat lines structured for journalist + LLM citation (pair with `/founder-pipeline:ai-seo` and `/founder-pipeline:ai-seo-llms-builder`: llms.txt, schema, quotable lines). BUILD blocks.
- **Free tools**: assessments, calculators, benchmarkers. BUILD blocks; tools earn passive "resources" links.
- **Definitive guides**: one canonical piece per keyword gap — the piece others cite instead of writing their own.

## 6. Non-standard plays

- **Badge embeds** (biggest asymmetric win — for brand and AI-citation surface, NOT PageRank): a "Member" badge for member companies, a "Speaker @ {event} {year}" badge for every speaker's site, a "Listed in {directory}" badge for directory members. Snippet ships with `rel="nofollow"` baked in, brand alt text. If a host chooses to add a followed editorial link themselves, that's their call — never instruct it. DEPENDENCY: badge asset + landing pages must exist → BUILD block first; outreach gated on it.
- **Awards**: a named award in your category — winners get a badge + award page. Same nofollow + BUILD rules as badges.
- **.edu links**: university guest lectures → course/speaker pages. Check exclusions first (some go dead between campaigns).
- **Testimonial links**: tools the owner actually uses — keep that list wherever you keep vendor notes and point the block at it. Executor drafts from real usage notes; OWNER-ONLY approval verbatim before anything is sent — their name on a vendor homepage is permanent.
- **Newsletter swaps**: mention swaps with peer newsletters — real audience value; newsletter web archives ARE crawled, so archived swap links follow the Law 4 nofollow rule (same as family 2).
- **Wikipedia (notability path ONLY)**: never edit your own links in. Linkbait asset → press citations → independent editors. Anything else violates Law 1. See Family 7 for the entity groundwork that precedes it.

## 7. Entity SEO / Knowledge Graph (identity consolidation — NOT backlinks)

These shape how Google and LLMs understand *who the person and the organisation are*; they do not pass PageRank. Every item here is `nofollow` or not a link at all (a SERP feature). **NEVER count them as referring domains, report them as backlinks, or put them in the link ledger** — track them in a separate "entity" line. Success = knowledge-panel eligibility + accurate AI answers, not DR. Prioritize for personal brand and org brand; low priority for SaaS.

- **Wikidata item (do FIRST — the foundation)**: create/extend the Q-item for the person and for the organisation. Statements: occupation, employer, alma mater, board roles, official website, and `sameAs` to authoritative profiles. **Cite each statement to an independent source** (press, conference pages, a company-data platform) — unsourced promotional items get deleted. OWNER-ONLY signup/edit; executor drafts the statement list + sources. Wikidata is the primary feed for Google's Knowledge Graph and a growing LLM grounding source — highest-leverage entity move.
- **Google Knowledge Panel**: once the entity is consistent across Wikidata + `sameAs`, claim the panel on the person's name via Google account verification. OWNER-ONLY. Owns the right-hand SERP box; no link value.
- **`sameAs` consistency audit (on-site)**: the Person/Organization JSON-LD on the personal-brand site and every property's About page must list the SAME canonical profile set everywhere (LinkedIn, YouTube, GitHub, the company-data profile, and the Wikidata Q-item once live). Mismatched/missing `sameAs` weakens entity resolution. On-site fix → BUILD block.
- **Company-data platforms (person + org) — always claim/complete both**: the person profile AND the organisation profile on the major startup/company database. Fill website, one-line description, and the offerings/service fields (this is the **service-highlight** surface — that text is scraped into LLM and investor-tool answers about "who is X / what do they do"). Link the profile from the Wikidata item via the platform's external-ID property. Links are nofollow — value is entity-graph strength + AI-answer accuracy, not PageRank. Keep name spelling identical to every other profile.
- **Other authoritative profiles that feed the entity**: ORCID/Google Scholar if talks or papers are indexed, consistent speaker-page name spelling. All nofollow; value is entity-graph strength.

## Scoring guidance

Impact H = DR 50+ editorial, or repeatable at scale with real traffic value; M = DR 20-50 relevant; L = below, or pure-directory noise.
Fresh-playbook priority: unlinked mentions → fix requests → event listings (conference) → directory invites → one-way placements → PR pitches → badges (after BUILD) → linkbait assets.
Family 7 (entity) is scored separately — not on DR. Rank it by knowledge-graph leverage: Wikidata item → sameAs audit → Knowledge Panel claim → supporting profiles. For personal/org brand, the Wikidata item ships early (it's a prerequisite for the panel and for any future encyclopaedia article), even though it passes no link value.
