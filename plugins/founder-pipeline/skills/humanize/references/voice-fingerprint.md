# Voice fingerprint — template and worked example

A fingerprint is a stylometric record of how one author writes when nobody edits them. It does two
jobs the forbidden-words list cannot:

1. **Stops the editor scrubbing features that are genuinely theirs.** Half of what a de-AI checklist
   flags is somebody's actual habit.
2. **Lets fresh prose written on their behalf carry their hand** — the attested constructions, at
   the attested frequency.

Ship the filled-in version at `brand_context/voice-fingerprint.md` in the workspace. This file is the
template plus one worked example; do not edit copy against the example.

---

## How to derive one

- **Corpus:** 10–15 pieces the author wrote by hand, spread over several years. Exclude anything
  AI-assisted, ghostwritten, or copy-edited by someone else. If you cannot establish provenance,
  exclude it — a fingerprint built on an editor's habits is worse than none.
- Where the author has published both hand-written and pipeline-written material under the same
  name, separate the two piles first. The contrast between them is the most useful data in the whole
  exercise (section 3 below).
- Read for what **repeats**, not for what is good. A brilliant one-off line is not a fingerprint; a
  mediocre construction appearing in nine pieces out of eleven is.
- Have the author confirm the result. They will disown a feature or two, and approve others you
  would not have dared to keep.
- Refresh yearly, or after any deliberate change of register.

---

## Template

### 1. Fastest authenticity discriminators, ranked

The few features that, when present, make the text almost certainly theirs — and whose absence
across a whole body of published work is itself evidence of a pipeline. Rank them; the editor reads
the top three most often.

Prompts to fill it: their one unmistakable punctuation habit · one syntactic construction they own ·
second-language residue, if they publish outside their first language · their preferred discourse
markers and contrast connector · how they carry evidence (numbers? names? neither?) · capitalisation
and formatting quirks · how they end a piece.

### 2. Genuinely theirs — never flag as AI tells

Features that look like machine tells on a checklist but are attested in the corpus. Each entry
needs a count or a "seen in N of M pieces", so a future editor can trust it.

### 3. Known machine signatures on this author's own corpus

What outed the AI-written pieces already published under their name. Written per era, because the
tells move. Two eras most corpora show:

- **Gloss era** — AI vocabulary clusters (crucial / pivotal / meticulously), "isn't just X; it's Y"
  closers, recap bows, "In the dynamic world of…" openers, layered over the author's real skeletons.
- **Pipeline era** — the first-order tells scrubbed (no em dashes, no flagged vocabulary) but: one
  epigram per paragraph sustained without a single flat stretch, fragment-contrasts ("Not a title. A
  scope."), a pull-quote per section, uncontracted register, manufactured-dread openers, an
  identical scaffold across every post, coinages recycled verbatim between posts, zero
  second-language residue, and FAQ blocks repeating body sentences word for word.

### 4. How to write as them

Two or three paragraphs of operating instruction, ending with the dosage rule from `SKILL.md`.

### 5. Approved plausible slips

**Requires the author's explicit written approval before a single one ships.** Small grammar slips
they would plausibly make but the corpus does not happen to attest. Grammar only, never spelling.
Max one per piece; most pieces carry none. Never in a headline, a price, a name, or a sentence whose
meaning the slip could bend. List what is approved *and* what was explicitly rejected as below their
level — the rejections stop a future editor re-litigating it.

---

## Worked example (fictional)

**The example author:** a Czech-speaking engineering consultant who publishes English blog posts on
their own site. Corpus: eleven hand-written posts written over four years, plus two recent posts they
confirmed were untouched. Second-language English, technical audience, no editor. Everything below is
invented to demonstrate the shape — replace all of it.

### 1. Fastest authenticity discriminators, ranked

1. **Zero em dashes.** Never one in body prose. Where a dash belongs they glue a bare hyphen to the
   next word. An em dash under their byline means someone else edited it.
2. **Missing-"that" constructions** ("The problem is, nobody owns the runbook") and verbless
   openers ("Which is the whole point.").
3. **Second-language residue left standing**: "help you to", "invest into", "discuss about", "on a
   weekly basis", article slips, occasional agreement errors.
4. **Signature connectives:** "as opposed to" as the contrast connector of choice; paragraphs opened
   with "In practice," / "Long story short," / "That said,".
5. **A real number or name in nearly every claim** — team sizes, percentages, tool names. Fractions
   written as digits.
6. **Capitalised concept-nouns** mid-sentence: Product, Values, Mission.
7. **Abrupt endings**: a question back to the reader, a teaser for the next post, or a bare
   lessons-learned list. Never a recap, never "In conclusion", never a polished CTA paragraph.

### 2. Genuinely theirs — never flag as AI tells

- Rule of three and imperative triads (attested in 8 of 13 pieces)
- Cleft contrasts and aphorism ladders — their genuine rhetorical mode, not a generator tic
- Question-as-transition ("Why?", "The outcome?") and dense direct reader questions
- Heavy mid-sentence bold, numbered tips, one-to-four-sentence paragraphs
- Emoji in body text and in headers; parentheses carrying examples
- One flagged vocabulary word that appears five times in the hand-written corpus — exempted by name
  in `forbidden-words.md` rather than scrubbed
- Blunt negativity, occasional profanity, sarcasm in scare quotes, self-criticism runs
- Mixed British/American spelling; contractions throughout — they never write "do not / It is /
  cannot" in prose

### 3. Known machine signatures on this author's corpus

The two eras described in the template both appear, the pipeline-era batch most recently: seven
posts on an identical scaffold, one coinage repeated verbatim across four of them, a fixed
credibility paragraph pasted into every post, and zero second-language residue in an author whose
hand-written corpus produces it in every piece. That last one is what settled it.

### 4. How to write as them

Draft from their real material — notes, transcripts, numbers from their published record. Keep their
sentences wherever they exist; their phrasing verbatim beats any imitation. For fresh prose:
contract, connect clauses with commas where a period would be "cleaner", let one sentence run too
long, open a paragraph with "In practice," or a question, end at least one section flat, and stop
the piece before it feels finished.

Fresh prose also carries their second-language residue, governed by the `SKILL.md` dosage rule: two
or three constructions from the discriminators list per piece, varied between pieces. Zero across one
post is fine. Zero across eleven posts is a signature — the pipeline's, not theirs.

### 5. Approved plausible slips

Approved by the author in writing, dated in their own file:

- Article slip: omitted or wrong article ("a feedback from the team")
- Verb-preposition calque: "discuss about the roadmap", "it depends what you measure"
- "explain me" / "recommend you to" ("let me explain you the trade-off")
- "from my experiences" where English wants the singular
- Adverb placement: "we discussed it already yesterday", "I know very well this pattern"

Explicitly rejected as below their level, reads as fake: dropped third-person -s, tense chaos,
spelling errors, double negatives, uncountable plurals ("informations").
