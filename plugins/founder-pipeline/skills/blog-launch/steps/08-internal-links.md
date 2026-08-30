# Step 08 — Internal links INTO the new post

Links FROM the post were placed in steps 03-04. This step is the reverse: **at least 3 existing pages/posts link TO the new post** (old-guide rule: "add new blog post to 3 internal links"). New posts with zero inbound internal links are orphans for crawlers and readers alike.

Runs after the gate passes, **in parallel with step 07 (translate)**. A mid-tier model in a subagent is enough for candidate discovery; the edits themselves are trivial and stay in the main loop. Changes ride the SAME commit/deploy as the post itself (step 09), so everything ships in one deploy.

## Find candidates (subagent)

Grep the site repo for existing content that mentions the post's topic terms:

1. **Existing blog posts** (every language you publish in) whose body touches the topic — the best link is inside a sentence that already discusses it.
2. **Service/persona pages** where the post answers a question the page raises (e.g. a role-definition post ← the matching persona mentor page).
3. **The knowledge page** if the post fits its lists.

Rank by topical fit + page traffic (money pages beat old posts). Return top 5 with the exact sentence/section where the link lands.

## Place (main loop, 3-5 links)

- Anchor text = meaningful phrase (the post's claim or keyword), never "read more" / "click here".
- Weave into an EXISTING sentence where possible; add at most one new sentence per page. Match the page's language (a translated page links the translated mirror).
- Mind your templating language's inline-link whitespace rules in component files; in MDX, plain Markdown links.
- Bidirectional check: if the post links a persona page (step 04), that persona page linking back is the highest-value pair.

Record the placed links in `STATE.md`. Build once to verify. **Next:** `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/08b-review-pr.md` — the privacy gate runs before anything is pushed, then the PR + preview go to a named delegate via your task board. The inbound-link edits are part of what they review.
