# P4.S0 — Email provisioning → `P4-Build.S0-Email.md`

**Phase: P4-Build** (opens the phase)

**Numbering note (deliberate exception):** every other step in this skill is S1+, no letter suffixes, no S0 — see SKILL.md's "Step IDs" section. This step breaks that convention on purpose: it must run before P4.S1-Keywords (which seeds `TRANSLATION-GLOSSARY.md` and the keyword contract that copy/web trace to) and before P4.S3-Web (whose contact-page copy and transactional sending domain both assume real inboxes already exist), but inserting it as a genuine S1 and shifting Keywords→S2, Copy→S3, Web→S4, SourceGap→S5, Deck→S6 would renumber every cross-reference to those steps across the skill AND retroactively invalidate any in-flight stream that already has an approved P4.S2/S3 under the old numbers. Breaking a live stream's history is worse than one odd step number. Do not "fix" this by renumbering later without checking every active `PROGRESS.md` first.

**Earns its keep when** the stream needs a real inbox people can reply to — which is every stream with a public web presence or outreach motion. Sequenced here because email needs the domain (locked at P1.S7-Name) and a DNS zone you control, and because P4.S2-Copy's contact/footer copy and P4.S3-Web's transactional-sending setup both assume the addresses already exist.

**Becomes performative when** the stream deliberately has no email presence of its own (e.g. a sub-brand section inside an existing repo that already inherits the parent's inbox) — record a one-line skip in `brief.md` naming which existing inbox the stream uses instead, and move to P4.S1-Keywords.

**Hard prerequisite:** the domain must be registered and its DNS zone must be under your control (a provider whose records you can edit yourself — the house stack declared at P1.S1 names which one) before this step opens. Both are P1.S7-Name's job (WHOIS + "register the matching domains same-day"). This step does not choose or register a domain; it provisions email ON the one P1.S7 already locked.

## Pattern: add the domain to a mail tenancy you already pay for, don't buy a new mailbox

The cost trap this step exists to avoid: paying a second per-seat mailbox fee for every new stream domain. Almost every business-mail provider lets one paid tenancy carry additional domains at no extra seat cost — the mechanism has a different name per provider, and picking the right one is the whole decision:

| Provider | The zero-extra-seat mode | What it gives you |
|---|---|---|
| Google Workspace | **User alias domain** (not "secondary domain") | Every existing user automatically gets the `@<newdomain>` twin of their primary address, free |
| Microsoft 365 | Added domain + per-user **alias** (proxy address) | Same shape: aliases on existing seats, no new licence |
| Fastmail / Zoho / Migadu and similar | Additional domain + aliases on the existing account | Same shape; alias caps vary by plan |
| A self-hosted or provider-agnostic setup | Virtual alias map | Same shape; you own the DNS either way |

**Google Workspace is the worked example throughout this step** because it is the most common case and its alias-domain mode is the easiest one to get wrong (choosing "secondary domain" instead of "user alias domain" silently starts billing per seat). If the stream is on another provider, keep the *shape* — add the domain to the existing tenancy, take the free-alias mode, publish MX/SPF/DKIM/DMARC — and swap the console steps for that provider's equivalent. **Nothing below depends on Google specifically except the click paths.**

If there is no existing tenancy at all, this step also covers the first one: pick a provider, buy exactly one seat, and treat every future stream domain as an alias on it.

**Ask one at a time:**
1. Confirm the domain (from P1.S7) and that its DNS zone is live where you can edit it (`dig NS <domain>` should return your provider's nameservers).
2. Which mail provider holds the existing tenancy (or, if none, which one is being bought)? Confirm the zero-extra-seat mode by name before touching anything — a wrong mode choice here is a recurring bill.
3. Which role addresses does this stream need beyond the automatic user-alias twins? (e.g. `hello@`, `hi@`, a named founder alias) — these become aliases on an existing user's account, not separate mailboxes.
4. Does this stream also need transactional sending (contact form, auto-replies) via a sending API? If yes, flag it now — the SPF record this step writes and the one P4.S3-Web writes for the sending provider MUST merge into one root TXT, never coexist as two. DNS permits only one SPF record per hostname; a second one silently breaks both senders. Most sending providers want their own sending subdomain (`send.<domain>` or similar) specifically to avoid this collision — confirm that's the plan before locking root SPF here.

**Setup (the owner's own click-through in the provider's admin console — not automatable, ~15 min once DNS has propagated). Google Workspace click paths shown; substitute your provider's equivalents:**
1. `admin.google.com` → Account → Domains → Manage domains → Add a domain → enter the stream domain → choose **"User alias domain"** (not a primary/secondary domain — alias is the free, zero-extra-seat option).
2. Verify ownership — the provider issues a TXT record; add it in the domain's DNS zone.
3. MX record per the provider's current published values (Google Workspace: `smtp.google.com`, priority `1` — a single-record setup). Take the values from the provider's own docs at the time you run this, not from memory; MX values do get revised.
4. SPF: one root TXT authorising the mail provider (Google Workspace: `v=spf1 include:_spf.google.com ~all`) — **check ask #4 above first; merge with any existing/planned transactional-sender SPF instead of creating a second root TXT.**
5. DKIM: generate the signing key for this domain in the provider's admin console (Google Workspace: Apps → Gmail → Authenticate email) → publish the resulting TXT in the DNS zone.
6. Every existing user on the tenancy automatically gets the `@<newdomain>` twin of their primary address (same local part) — no action needed for that. For the extra role addresses from ask #3 (`hello@`, etc.): add them as alternate emails / aliases on the relevant existing user, **not as new seats**.
7. In the mail client: the new addresses become selectable as From identities (Gmail: Settings → Accounts → Send mail as — alias domains on the same tenancy need no SMTP password and no "verify" click). Pick the From address per send.

**Sender identity — make every address resolve to a full profile (name + photo), not bare initials:**
1. **Send-as display name:** set the full public name on every alias identity; never leave the bare address as the name.
2. **Account photo:** one photo on the account serves the primary AND all alias addresses — aliases share the account's profile; there is no per-alias photo on any of the major providers.
3. **Public visibility:** set the profile name + photo visibility to **anyone**, not contacts-only. Without this, non-contacts see initials even when the photo exists.
4. **Admin check (once per tenancy, probably already set):** confirm users are allowed to edit their own name/photo.
5. **Recipients on other mail platforms never read your provider's profile directory** — add the same photo on **Gravatar** for each public-facing address (role aliases + domain twins); one Gravatar account holds unlimited addresses.
6. **BIMI (domain logo shown in the recipient's inbox) is deliberately deferred:** it requires DMARC at enforcement (`quarantine`/`reject`), and this step ships `p=none` — queue BIMI together with the DMARC-ramp item in P6.S3, never attempt it at launch.
7. **Alias caveat to actually test:** avatars render most reliably for the primary-domain From; alias sends can fall back to initials for recipients who have never corresponded. The def-of-success test send must check the avatar/name renders in a *fresh* inbox, not just that delivery works.

**DMARC — deliberately NOT hardened at launch.** Publish `_dmarc.<domain>` at `p=none` (monitor-only) alongside step 4 above so the record exists and reports flow, but do not ramp toward `quarantine`/`reject` here — that is a weeks-long monitored process, not a build task. The ramp pattern, for the P6.S3 item:

- Point `rua=` at an aggregate-report mailbox that actually parses the XML (Postmark's free DMARC digest, dmarcian, Valimail, or your provider's own DMARC dashboard — any of them, but not an unmonitored inbox).
- Inventory **every** legitimate sender on the domain first (human mail, transactional API, newsletter tool, invoicing tool, calendar/booking tool). A sender you forgot is the one that breaks when you ramp.
- Ramp `none → quarantine 25% → quarantine 100% → reject`, with **2+ clean weeks** between steps — clean meaning every legitimate sender shows an aligned SPF *or* DKIM pass in the aggregate reports.
- Never jump straight to `reject`. Rolling back a `reject` that bounced a week of real mail is not a rollback; the mail is gone.

Record this stream's domain as a dated P6.S3 90-day-plan item; do not block P4 on it.

**Skills:** none — this is direct DNS + mail-admin console work, no specialist skill wraps it.

**Write to** `P4-Build.S0-Email.md`. Record: the domain + confirmed editable DNS zone, the mail provider and the exact tenancy mode chosen (with the words the provider uses for it), MX/SPF/DKIM values as actually published (not the template — paste the real TXT/MX content), which role addresses were added as aliases and to which user, the `_dmarc` record at `p=none` and where its reports land, and — if a transactional sending domain is also planned — the exact merged-SPF value both this step and P4.S3-Web must ship (write it here first so P4.S3 cites it instead of re-deciding it).

**Def-of-success — ALL must pass before Owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- Domain confirmed registered + DNS zone editable by you before this step opened (cite P1.S7).
- Domain added to the existing mail tenancy in the **zero-extra-seat mode** (Google Workspace: a *user alias domain*, not primary/secondary; equivalent mode named explicitly for any other provider) — ownership record published and verified. A mode that adds a per-seat charge fails this criterion unless the extra seat is deliberate and justified in the file.
- MX, SPF, and DKIM records live and verified via `dig`, not just "saved in the console."
- Every role address the stream needs (ask #3) exists as an alias and sends from the mail client — tested with one real sent message per address.
- Sender identity set: display name on every alias, account photo published with visibility set to anyone, Gravatar covering the public role addresses — verified by a test send to an inbox that has never corresponded with the address (full name + avatar render, not a bare address or initials).
- **If transactional sending is also planned:** the merged SPF value is recorded here and matches exactly what P4.S3-Web will ship — one root TXT, not two.
- `_dmarc` published at `p=none` with a working `rua` aggregate-report address that is actually monitored — not left unset, not jumped straight to enforcement.
- The DMARC-ramp follow-up is queued as a dated P6.S3 90-day-plan item, not silently dropped.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P4-Build.S0-Email.md`.
2. Invoke `/critical` on the draft — attack anything recorded as "done" that wasn't verified live (a saved console setting is not the same as a resolving DNS record), and any SPF/DMARC value that wasn't actually tested with a real sent message.
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Email live on [domain]: MX/SPF/DKIM verified, [N] role addresses provisioned, DMARC at p=none reporting to [rua]. Keywords next — copy/web can now reference real addresses. Approve, or add more role addresses first?"

**Next:** `stages/P4-Build.S1-Keywords.md`
