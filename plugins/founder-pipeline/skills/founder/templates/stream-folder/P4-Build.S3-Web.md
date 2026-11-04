# Web build — log + status

**Stream:** [slug]
**Step:** P4.S3-Web (P4-Build)
**Last updated:** [date]

> Default: **your declared house stack (P1.S1), built via `/web-site-creator` — always.** The stack this pipeline was built against, and its recommended default, is a static-site framework deployed to an edge host. A web build outside your declared house stack needs the owner's explicit call, recorded here + in P2-Viability.S2-Tooling.md with the reason.

---

## Gates

- BUILD: proceeds in every run. There is no pre-sale gate on the build itself — the pre-sale evidence gate lives at P2.S4 and again at P6.S3.
- Copy sources section of P4-Build.S2-Copy.md approved: [yes/no — date]

## Build

- Pipeline: [`/web-site-creator` | other — name it and record why]
- Repo + `web/` location: [...]
- Deploy target: [domain/path]
- Live URL: [...]

## Hardening results

| Check | Skill | Result / skip reason |
|---|---|---|
| Technical SEO | `/seo-audit` | |
| AI-search visibility | `/ai-seo` | |
| Performance (95+ mobile) | any Lighthouse/CWV pass. `/cloudflare:web-perf` covers it if you have the `cloudflare` plugin installed — optional dependency | |
| Voice pass | `/brand-voice` | |
| Design review | inline: read every page as a first-time ICP visitor. Check hierarchy (one obvious next action per screen), contrast and tap targets, mobile at 375px, empty/error states, and that nothing on screen is placeholder. Anything you would not send to a prospect is a defect, not a nit | |

## Copy-match diff (rendered text vs Copy sources — returned by the build subagent, per page)

| Page | Verdict (match / deviation) | Quote |
|---|---|---|
| | | |

## Wiring verification (live evidence)

- Form/transactional-email test submission — message ID: [...]
- Test event visible in your analytics tool: [event name — link/ref]
- `dig` output — SPF / `_dmarc` / DKIM selectors: [pasted]

## Handoff to Activation

Launch execution (indexation, engines, blog posts, MCP/skill publication, magnet distribution) is P5.S1; backlinks + internal mesh are P5.S2. This step only records:

- [ ] Analytics instrumentation live (this step owns the wiring, once)
- [ ] Site handed to P5.S1 with live URL + sitemap verified

## Open placeholders

- [asset] — owner: [...]

---

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
