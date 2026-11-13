# Learnings entries (seed)

This file belongs to the `seo-audit` skill.

- 2026-08-22 · any page · all — **A high score and a failed Launch Gate are independent, and the
  common case.** The checker's own demo page scores 100 and fails the Gate on thin content. Action:
  never report the score without the Gate line beside it, and never let a client trade one for the
  other.
- 2026-08-22 · homepage / dashboard blocks · all — **live-data widgets served the literal string
  "Loading…" to GPTBot and Googlebot.** Two separate sites, same bug, one logged here
  and one in `/founder-pipeline:ai-seo`. Action: on any page with a counter, chart or "live" block,
  run `crawler_fetch` before grading anything else — the widget must server-render its real value
  and let JS *replace* it, never the reverse.
- 2026-08-22 · service pages · all — **the offer shape fails before the SEO does.** Two services
  combined on one page defeats the one-primary-keyword model no matter how clean the metadata is.
  Action: run the Money Page checklist before the on-page layer on any commercial site, and lead
  the report with it when it fails.
