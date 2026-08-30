# Step 10 — Syndicate to your republish set (+ social via step 12)

**Declare a standard republish set once, then stop re-deciding it per post.** The worked default here is Medium + Substack + Hackernoon + a professional social network; substitute whatever platforms your audience actually reads. Once declared, no per-post confirmation is needed for the set itself — GATE B approval of the post covers it. The social post runs through step 12's drafts (pick the strongest variant and post it).

Two phases: exports (can prep pre-deploy with a canonical placeholder) and posting (needs the live URL). Load `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/references/syndication-specs.md` for per-platform rules.

## Phase 1 — exports (small/fast-model subagents, parallel; may start right after the gate passes)

Generate `exports/medium.md`, `exports/substack.md`, `exports/hackernoon.md` per the specs: absolute site URLs for every internal link, per-platform title/intro tweak, attribution footer, image list with local file paths for upload, and the canonical URL (placeholder `{{CANONICAL}}` until deploy fills it).

## Phase 2 — post via browser automation (default)

After deploy, drive a browser-automation tool in the owner's already-logged-in browser. (Browser automation is an optional dependency — if you don't have it, every platform below falls back to pasting the export file by hand, which is exactly why the exports exist.)

1. Check existing browser tabs first; new tab per platform.
2. **Medium**: prefer the import tool (`medium.com/p/import` with the live URL — sets canonical automatically); fallback: new story, paste export, set canonical in Advanced settings. Tags per spec. **Publish**; fall back to draft only if canonical can't be set.
3. **Hackernoon**: new draft, paste, fill the canonical field, save as draft for editorial review.
4. **Substack**: DO NOT post same-day. Schedule per spec (7-14 days after original, "Originally published at..." first line). Create the draft now, scheduled or dated, never immediate-send to subscribers without the owner's explicit word.
5. Screenshot each created draft; report URLs.

**Brittleness rule:** any login wall, 2FA, captcha, or changed editor UI → stop that platform after 2 attempts, tell the owner which export file to paste manually (the exports ARE the fallback), continue with the next platform. Never leave a half-filled post published; drafts only.

Update `STATE.md` (per-platform: draft URL / scheduled date / handed to the owner). Runs ∥ `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/11-backlinks.md` and `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/12-announce.md`.
