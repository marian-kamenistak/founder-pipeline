export const meta = {
  name: 'judge-panel',
  description: 'Independent gate critics judge one step file against its criteria, one per framing, and the gate passes only if all pass',
  whenToUse: 'A founder-pipeline kill gate (P1.S1, P2.S4) that needs opposing framings judged independently, or any step that wants more than one blind critic.',
  phases: [{ title: 'Judge', detail: 'one gate-critic per framing, blind to the others' }],
}

// args: { artifactPath: string, criteria: string[], framings?: string[] }
// Each critic reads the file itself in a fresh context. The script never passes one critic's
// answer to another, so no framing can anchor the rest.

const input = args || {}
const criteria = input.criteria || []
const framings = input.framings && input.framings.length ? input.framings : ['unframed']

if (!input.artifactPath || !criteria.length) {
  throw new Error('judge-panel needs args { artifactPath, criteria: [..], framings?: [..] }')
}

const PANEL = {
  type: 'object',
  required: ['verdicts', 'blocking', 'gate', 'score'],
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        required: ['criterion', 'pass', 'evidence'],
        properties: { criterion: { type: 'string' }, pass: { type: 'boolean' }, evidence: { type: 'string' } },
      },
    },
    blocking: { type: 'array', items: { type: 'string' } },
    gate: { type: 'string', enum: ['PASS', 'FAIL'] },
    score: { type: 'number' },
  },
}

phase('Judge')
const answers = await parallel(
  framings.map(framing => () =>
    agent(
      `Step file to judge: ${input.artifactPath}\nFraming: ${framing}\n` +
        `Def-of-success criteria:\n${criteria.map((c, i) => `${i + 1}. ${c}`).join('\n')}\n` +
        'Judge every criterion PASS or FAIL with one line of evidence. A criterion without evidence is FAIL.',
      { label: `critic:${framing}`, phase: 'Judge', agentType: 'founder-pipeline:gate-critic', schema: PANEL },
    )),
)

const panels = answers.map((a, i) => {
  if (!a) return { framing: framings[i], gate: 'FAIL', score: 0, verdicts: [], blocking: ['critic returned nothing'] }
  // The gate is computed from the verdicts, never taken from the critic's own summary line:
  // every criterion must be judged, every one must pass, and nothing may be blocking.
  const judgedAll = a.verdicts.length >= criteria.length
  const allPass = a.verdicts.every(v => v.pass)
  const gate = judgedAll && allPass && !a.blocking.length ? 'PASS' : 'FAIL'
  return { framing: framings[i], gate, score: a.score, verdicts: a.verdicts, blocking: judgedAll ? a.blocking : [...a.blocking, 'not every criterion was judged'] }
})

return {
  artifactPath: input.artifactPath,
  // One failing framing fails the gate. A panel never averages.
  gate: panels.every(p => p.gate === 'PASS') ? 'PASS' : 'FAIL',
  panels,
}
