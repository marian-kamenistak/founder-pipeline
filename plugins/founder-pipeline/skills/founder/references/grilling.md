# Grill pass — how the ideation steps ask questions

Reference for the `founder` skill. Read it before the questions of any P1-Ideation step. The stage file lists what the step must settle; this file says how to ask.

Adapted from the `grilling` skill in [mattpocock/skills](https://github.com/mattpocock/skills) (MIT): the design tree, the frontier, facts versus decisions, and a recommended answer with every question. The pipeline keeps its own limits on top: at most 6 questions asked per step, one at a time, and the step's def-of-success still decides the gate.

## Why

An idea in ideation is a tree of decisions. Which problem decides which buyer, the buyer decides the alternatives, the alternatives decide the offer. Asking them in the order they came to mind produces answers that contradict each other two steps later, and the contradiction then surfaces as a loop-back. The grill pass asks them in dependency order, and only asks what a person has to decide.

## The pass, in order

1. **Map the tree before asking anything.** List the decisions this step must settle (the stage file's questions and def-of-success criteria are the starting list) and note which depend on which. Keep the map to yourself; the owner sees questions, not the map.

2. **Sort facts from decisions.** A fact is anything a source can answer: the intake folder and `INTAKE.md`, `brief.md`, an approved earlier step file, a connected tool listed in `CAPABILITIES.md`, a web search. Look facts up, with a `founder-pipeline:evidence-scout` when it takes more than one read. Never ask the owner for a fact. A decision is a choice only the owner can make: which pain to bet on, which segment to exclude, what to give up.

3. **Ask the frontier only.** The frontier is the set of open decisions whose prerequisites are already settled. Two decisions where one depends on the other never go out together: ask the first, let the answer reshape the second.

4. **Every question carries one recommended answer.** State the question in a line, then "Recommended: …" with the evidence it rests on (the intake line, the earlier file, the source). The owner can accept with one word. When the evidence argues against the way the stage file frames the question, say so and recommend against the framing.

5. **One at a time, at most 6 asked.** Looked-up facts do not count against the 6. If the owner asks for them together, send the current frontier as one numbered round and take the answers by number. If more than 6 decisions are still open, the intake is too thin or the step is doing two steps' work: say which, and fix that instead of asking a seventh.

6. **Play it back before drafting.** When the frontier is empty, restate the settled decisions in at most 5 lines and ask whether that is the shared understanding. Do not draft the step file until the owner confirms. A draft written on an unconfirmed playback is the thing this pass exists to prevent.

7. **Log the decisions in the step file.** One table at the top of the Validation loop block, so the critic can check the draft against what was decided:

   | Decision | Recommended | Owner's answer | Evidence |
   |---|---|---|---|

   Mark every row where the owner chose against the recommendation. Those rows are where the critic looks first.

## What it does not change

- The stage file's def-of-success. The grill pass improves the inputs; the gate still runs on the output.
- The honesty rules. A recommended answer that rests on a number cites the number's source or says `[assumption — validation: …]`.
- Unattended mode. With nobody to ask, answer each decision from the evidence, tag it `[assumption — owner review]`, and list it in `MORNING-REVIEW.md`, as `references/overnight.md` already requires. The playback in step 6 becomes the first section of the review packet.
