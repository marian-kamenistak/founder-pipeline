# Automation execution — browser mechanics, hard stops, and platform gotchas

`SKILL.md` Phase 4 is the *sequence*; this file is the *how*. `method.md` is the short version folded into the category playbooks.

**Read Law 5 first.** The agent submits genuine anonymous forms; the agent never authenticates. Account creation, password entry and SSO login are owner-only, and no in-chat authorization changes that — it is a platform rule. `/founder-pipeline:web-backlinks` Phase 4.4b carries the full reasoning, including the reversal of an earlier design that did try to automate signups. Nothing below is a workaround for that boundary.

## Credentials — what the agent may and may not touch

| Situation | What happens |
|---|---|
| Public form, no account, no login | Agent fills and submits, after asking in chat for a clear yes on that specific submission |
| Target needs a **new** account | OWNER-ONLY. Agent prepares the complete pack (copy at the right length, canonical NAP, asset URLs, cross-links) as paste-ready content. Owner signs up. |
| Target needs login to an **existing** account | OWNER-ONLY for the login step. If the owner authenticates and stays at the keyboard, the agent may drive the post-login non-secret form-fill in that same session. |
| Any password, passphrase, OTP, or recovery code | Never enters the agent's context, from any source, including a password-manager CLI. |

Keep a plain record of which platforms already have an account for which property — a note file or a
tag in the owner's password manager, maintained by the owner — so a run never proposes a duplicate
account under a different email. The agent reads that record; it does not write credentials to it.

## Browser automation — submission flow

Requires a browser-automation MCP server (e.g. `claude-in-chrome`), an optional dependency you install separately. Without one, every target becomes a prepared pack for the owner.

Load the tool set once per session before use — a single batched call, not one per tool:

```
ToolSearch: "select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__form_input"
```

1. `tabs_context_mcp` first — check what's already open. Don't reuse a tab that isn't explicitly for this task.
2. `tabs_create_mcp` a fresh tab, `navigate` to the target's `submit_url` from `config/targets.json`.
3. `read_page` to see what the form actually asks for — never assume the fields match what was researched; sites change. This step is also where you find out whether the target is genuinely form-only or account-gated. A "self-serve" label written from search data rather than a live page load is not evidence, and has already been wrong in practice.
4. If the page shows any sign-in, sign-up or SSO requirement → stop, this is owner-only (Law 5).
5. Fill the listing form from `entity-pack.md`: the property's copy tier at the length the form asks for, the canonical email, the favicon/og:image URLs from the visual-assets table (download-and-upload if the form wants a file rather than a URL — `file_upload` or `upload_image` where the tool supports it).
6. **Before clicking final submit, check the page for any of the hard-stop conditions below.** If none are present, ask in chat for a clear yes on this specific submission, then submit.

## Hard-stop conditions — detect, screenshot, queue OWNER-ONLY

Do not attempt any workaround for these — that includes not trying a second CAPTCHA attempt, not guessing at a phone number, and not entering real payment data even if it's "just for verification."

| Condition | What it looks like | Action |
|---|---|---|
| Account creation / login | Any sign-up, sign-in, or "continue with Google/LinkedIn" gate | Stop — owner-only, Law 5 |
| Password field | Any password, passphrase or OTP input | Stop — never fill, from any source |
| Payment field | Any card number, billing address, or "Add payment method" step | Stop immediately, don't fill anything in that field even partially |
| CAPTCHA | reCAPTCHA, hCaptcha, a bot-challenge interstitial, or a generic "prove you're human" puzzle | Stop — don't attempt to solve it |
| Phone/SMS/ID verification | "Enter the code sent to your phone", ID upload, liveness check | Stop — this needs the owner's device |
| Ambiguous link-back term | Terms mention a "verification badge", "featured link", or similar that isn't clearly optional | Stop, don't guess — read the full terms page first if unclear, then stop if still ambiguous |

On any hard stop: capture the exact state with a screenshot, note the path, and create the ledger row with that detail per `SKILL.md` Phase 4 step 4. Log the same to `<property>/listings/runs.jsonl` with `outcome: "hard-stop"`.

**A hard stop found late is still a finding worth recording.** Two patterns show up repeatedly and both were originally catalogued as "free": a launch platform whose free tier turns out to be paid-only once you reach the actual launch modal, and a directory whose free basic profile has since become a paid tier. Correct the `targets.json` row when you find one — the stale "free" label is what sent the run there.

## Live-check verification

Never mark a row `Done` on the assumption a submission succeeded. After a submission — or after the owner confirms one they completed manually — fetch the actual listing URL and confirm the property's name and description actually appear. Log the live-check result in the jsonl entry and record `listing_url` on the `targets.json` row, which is what makes the listing checkable by `nap-audit` later.

## Known browser-automation limitations

- **Native `prompt()` / `window.open` file-URL pickers freeze the tab.** Some "Paste a URL" image-upload controls call a native browser `prompt()` rather than opening an in-page input. This blocks the renderer's JS thread entirely — mouse-event dispatch and script evaluation both time out (30–45s), and screenshots fail with a script-injection timeout until the dialog is dismissed. It is NOT a frozen tab in the usual sense; pressing a key that reaches the native dialog can clear it, but the tool calls can't see or target the dialog itself. If this happens, ask the owner to look at the actual browser window and dismiss or fill the dialog themselves — don't keep retrying clicks, each retry likely queues another native prompt.
- **`navigate` cannot load `file://` URLs** — the extension lacks file-scheme access, and the tool also mis-prepends `https://` to a `file://` string regardless. To render a local HTML file (e.g. a custom-built graphic to screenshot), serve it over a throwaway local HTTP server instead: `python3 -m http.server <port>` from the file's directory, then `navigate` to `http://localhost:<port>/file.html`. Kill the server when done.
- **Building a real gallery/OG image beats an auto-generated one.** Several launch platforms auto-generate a marketing banner from the submitted URL using stock photos of "team members" who don't exist at the company, plus invented copy. That is fabricated imagery — remove it and replace with a banner built from real assets (the property's own logo, a real headshot, figures from your numbers source only). A simple HTML/CSS file rendered via the local-server trick above, screenshotted and uploaded, is a fast repeatable way to do this without a design tool.

## Wikidata: when the statement-editing UI won't render

A freshly-created, fully-empty Wikidata item can render its "Statements" heading with nothing under it — no edit pencils, no "+ add value" / "+ add statement" buttons, on any browser or viewport, even fully logged in with a valid, edit-capable session (`mw.config.get('wgIsProbablyEditable')` returns `true`). Diagnosed via `mw.loader.getState('jquery.wikibase.statementview')` returning `null` (the module never registered) despite `wikibase.ui.entityViewInit` showing `loaded` — the interactive editing bundle simply didn't initialize on the empty item. Reload, resize and hover did not fix it.

**Workaround: call the Wikibase API directly from the page's JS context**, using the browser's own session cookie, no UI widget needed. The owner must be the one logged in — this rides an existing authenticated session, it does not create one.

```js
async function getToken() {
  const res = await fetch('/w/api.php?action=query&meta=tokens&format=json', {credentials:'include'});
  return (await res.json()).query.tokens.csrftoken;
}
async function createClaim(entity, property, snaktype, value) {
  const token = await getToken();
  const body = new URLSearchParams({action:'wbcreateclaim', entity, property, snaktype, token, format:'json'});
  if (value !== undefined) body.set('value', JSON.stringify(value));
  const res = await fetch('/w/api.php', {method:'POST', credentials:'include', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body: body.toString()});
  return res.json(); // .claim.id is the new statement's GUID
}
async function setReference(statement, url) {
  const token = await getToken();
  const snaks = JSON.stringify({P854:[{snaktype:'value', property:'P854', datavalue:{value:url, type:'string'}}]});
  const body = new URLSearchParams({action:'wbsetreference', statement, snaks, token, format:'json'});
  const res = await fetch('/w/api.php', {method:'POST', credentials:'include', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body: body.toString()});
  return res.json();
}
```

Value shapes: `wikibase-entityid` → `{"entity-type":"item","numeric-id":<N>,"id":"Q<N>"}`; `time` (dates) → `{"time":"+YYYY-MM-DDT00:00:00Z","timezone":0,"before":0,"after":0,"precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}` (precision 11 = day); plain strings (URLs, external IDs) → pass the raw string as `value`.

**Rate limit:** `wbsetreference` hits Wikidata's anti-abuse action throttle after 2 rapid calls (`actionthrottledtext`) — space reference-setting calls out, or expect to wait ~10 minutes and retry the remainder.

**Zero references is the default outcome to avoid.** An unreferenced claim reliably stays out of Google's Knowledge Graph and is low-trust for LLM grounding. Add a `P854` reference URL to every statement at creation time, not as a follow-up — use the entity's own site for definitional facts (org type, headquarters, founder) and the authoritative government registry for legal facts (country, incorporation date).

**Once real statements exist, the normal edit UI starts working again** — confirmed on reload after the API calls above. The broken state appears specific to a genuinely empty item.

## Not built yet

- **Unattended/scheduled execution.** The flow assumes a human is present for every credential-bearing step, by design. Making it unattended would require crossing the Law 5 boundary, so this is not a roadmap item — it is out of scope permanently for the credentialed half. The anonymous-form half could in principle be scheduled, but the per-submission confirmation rule means it still needs someone in the loop.
