# Email provisioning

**Stream:** [slug]
**Step:** P4.S0-Email (P4-Build) — deliberate numbering exception, see the stage file
**Last updated:** [date]

> Mailbox setup on the domain P1.S7-Name locked, using whatever hosted-email provider your house stack declares (P1.S1). Copy (P4.S2) and the contact/footer surfaces on the web build (P4.S3) both assume these addresses already resolve — this step runs first. If a transactional-email service is also planned, the merged SPF value recorded here is the one P4.S3-Web (Phase 3.2) must ship — never a second root SPF TXT.
>
> The values below are shown for a Google Workspace alias-domain setup as the worked example. Substitute your provider's own MX/SPF/DKIM values; the checks — resolve it live, send a real message — do not change.

---

## Prerequisite check

- Domain: [domain] — locked at P1.S7-Name, [date]
- DNS at your declared DNS host confirmed live: `dig NS [domain]` → [output / screenshot ref]

## Mailbox provider setup

| Step | Value | Verified |
|---|---|---|
| Domain added as | User alias domain | [ ] |
| Ownership TXT | [value] | [ ] `dig` confirms |
| MX | [provider's MX host + priority — e.g. `smtp.google.com`, priority 1] | [ ] |
| SPF | [full value — e.g. `v=spf1 include:_spf.google.com ...`, merged with your transactional sender if applicable] | [ ] |
| DKIM | [selector + value from the provider's admin console] | [ ] |

## Role addresses (user aliases)

| Address | Aliased to (user) | Send-as tested |
|---|---|---|
| | | [ ] real message sent |

## DMARC

- `_dmarc.[domain]` = `v=DMARC1; p=none; fo=1; adkim=r; aspf=r; rua=mailto:[aggregate-report address]`
- Ramp-to-enforcement queued: P6.S3 90-day plan, dated [date] — the pattern is `p=none` → collect aggregate reports for 2–4 weeks → `p=quarantine` at a low `pct` → raise → `p=reject`. Never jump straight to `reject` on a domain that already sends.

## Transactional sender interaction (if applicable)

- [ ] N/A — no transactional sending planned for this stream
- [ ] Transactional sending planned — merged SPF value above is what P4.S3-Web Phase 3.2 will ship; transactional sending subdomain: [value]

---

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Every recorded value verified live (`dig`, real sent message), not just "saved in console"
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
