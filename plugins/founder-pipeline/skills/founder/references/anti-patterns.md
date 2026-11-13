# Anti-patterns the pipeline refuses

Reference for the `founder` skill. Read it when a request looks like a shortcut around a gate, or when the owner pushes to skip one at a checkpoint. `SKILL.md` lists the short form; this is the full list with the reason behind each refusal.

## The list

- **Advancing without the owner's sign-off.** "Looks good, moving on" from the model is not approval.
- **Advancing on a failed def-of-success.** Any FAIL criterion means improvement loop. Also refused: grade inflation — re-running the critical pass softer to fish for a pass.
- **A funnel that never kills is a tunnel.** If early gates kill under ~20-30% of ideas, the gates are ritual. A killed stream is a WIN (avoided opportunity cost); the Camuffo RCTs (759 firms, Camuffo/Gambardella et al., large-scale replication of the "scientific approach to entrepreneurial decision-making" trials) show trained founders terminate MORE and earn more.
- **Locking a niche before the demand data.** P1.S4 exists so the niche, keywords, and content angles are picked FROM evidence — skipping it to "save time" re-creates the guess-first pipeline this version killed.
- **SEO/content as the first-revenue engine.** New pages have roughly 2-6% odds of top-10 within a year `[operating assumption]`; roughly 60% of first consulting clients come from warm network `[operating assumption]`. Keywords/web are 6-24-month compounders — never the plan for client #1.
- **Name before problem.** Force the name to fall out of ideation (and P1.S4's reframe data), not precede it.
- **Pricing from "psychological mechanisms"** instead of value × willingness-to-pay.
- **Business Model Canvas as deliverable.** Thinking tool, not output.
- **Polished brief from zero evidence.** A problem/ICP/offer claim with no cited data behind it — no prediction indicator, no named account, no real conversation, no benchmark — is fiction, however well-written.
- **Vanity KPIs.** Force one north-star *behavioral* metric.
- **"Everyone is the ICP."** Exclusion is a feature.
- **20-question intakes.** Cap at 6 per step, one at a time.
- **30-page outputs.** Produce the 1-pager that gets acted on.
- **Execution without validation gate.** No LOIs, no pre-sales, no pilots = no execute.
- **Building web/content and calling it launched.** A deployed site with unexecuted launch work (no posts, no registry submissions, no links) is inventory, not distribution — P5-Activation is execution, and skipping it re-creates the "drafted, awaiting" graveyard.
- **Web builds outside your declared house stack.** Every web surface goes through `/web-site-creator` on the stack declared at P1.S1, unless the owner explicitly overrides with a recorded reason. The point is not the specific framework — it is that one stack, chosen once, is what makes the build, the SEO hardening and the post-launch work repeatable.
- **Decks built outside the deck path.** P4.S5's default is HTML→PDF through a headless system browser, because the deck then shares the site's components, copy and prices instead of drifting from them, and regenerates from source on every change. A design-tool export (Canva, Figma, slides) breaks that link. Overriding the default is allowed; doing it without recording the reason in the step file is not.
- **Deciding the language late.** Which locales a stream serves is a P4.S1 decision, not a P5 afterthought. Retrofitting a second language means re-cutting every URL, 301ing the originals and re-earning their rankings. Locale is always a URL PREFIX (`/<lang>/<slug>`), never a suffix.
- **Writing `llms.txt` before the research.** An llms file assembled from the page tree describes the site; one assembled from P4.S1's query list answers what people actually ask Google and the AI engines. Only the second gets cited. `/ai-seo-llms-builder` enforces this: its `build` mode refuses to run without a query list, and its `audit` mode flags a file written from the page tree.
- **Accepting mediocre profit.** Under the hurdle rate or under the absolute floor at P2.S4 = KILL, not "kept small on the side".
- **Two streams in design at once.** Finish, park, or kill first.
- **Adding a stream without killing anything.** P1.S1 forces the portfolio trade before any design work.
- **Teaching frameworks instead of running them.**

## Why the honesty rules for numbers exist

Rule 2 is the one that pays. In one real run, a keyword check returned no data for five home-market terms and no data in any market for the category's own head term. Dropping those rows, or filling them with a small plausible number, would have hidden the most consequential finding of the run: the category the whole business was built around had no measurable search demand.
