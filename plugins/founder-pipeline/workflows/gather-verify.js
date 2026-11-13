export const meta = {
  name: 'gather-verify',
  description: 'One cheap scout per item, a skeptic on every load-bearing claim, then a completeness critic',
  whenToUse: 'A founder-pipeline research sweep over more than about six items: account enrichment (P3.S1), SERP sweeps per keyword cluster (P4.S1), competitor profiles (P1.S5).',
  phases: [
    { title: 'Gather', detail: 'evidence-scout per item, fixed fields, sources required' },
    { title: 'Refute', detail: 'claim-refuter per load-bearing claim, on the session model' },
    { title: 'Completeness', detail: 'completeness-critic asks what is missing' },
  ],
}

// args: { question: string, fields: string[], items: Array<string | {id: string, context?: string}>,
//         maxClaimsPerItem?: number }
// Model tiers are not set here. They come from the agent definitions in agents/:
// the scout runs on the small model, the skeptic and the critic inherit the session model.

const input = args || {}
const items = (input.items || []).map((it, i) =>
  typeof it === 'string' ? { id: it, context: '' } : { id: it.id || `item-${i + 1}`, context: it.context || '' })
const fields = input.fields || []
const maxClaims = input.maxClaimsPerItem || 3

if (!input.question || !items.length || !fields.length) {
  throw new Error('gather-verify needs args { question, fields: [..], items: [..] }')
}

const FINDING = {
  type: 'object',
  required: ['item', 'fields', 'claims'],
  properties: {
    item: { type: 'string' },
    fields: {
      type: 'array',
      items: {
        type: 'object',
        required: ['name', 'value', 'status'],
        properties: {
          name: { type: 'string' },
          value: { type: 'string' },
          source_url: { type: 'string' },
          accessed: { type: 'string' },
          status: { type: 'string', enum: ['VERIFIED', 'ASSUMED', 'NOT_FOUND'] },
        },
      },
    },
    claims: {
      type: 'array',
      items: {
        type: 'object',
        required: ['claim'],
        properties: { claim: { type: 'string' }, source_url: { type: 'string' } },
      },
    },
  },
}

const VERDICT = {
  type: 'object',
  required: ['claim', 'refuted', 'evidence'],
  properties: {
    claim: { type: 'string' },
    refuted: { type: 'boolean' },
    evidence: { type: 'string' },
    weaker_version: { type: 'string' },
  },
}

const GAPS = {
  type: 'object',
  required: ['complete', 'gaps'],
  properties: {
    complete: { type: 'boolean' },
    gaps: {
      type: 'array',
      items: {
        type: 'object',
        required: ['gap', 'next_action'],
        properties: { gap: { type: 'string' }, next_action: { type: 'string' } },
      },
    },
  },
}

const scout = item =>
  agent(
    `Item: ${item.id}\n${item.context ? `Context: ${item.context}\n` : ''}Question: ${input.question}\n` +
      `Fill exactly these fields: ${fields.join(', ')}.\n` +
      'Every field needs a source URL and an access date. NOT_FOUND is a valid answer. Never estimate a number.',
    { label: `scout:${item.id}`, phase: 'Gather', agentType: 'founder-pipeline:evidence-scout', schema: FINDING },
  )

const refute = async (finding, item) => {
  if (!finding) return { item: item.id, failed: true, fields: [], claims: [], verdicts: [], unchecked: 0 }
  const checked = finding.claims.slice(0, maxClaims)
  const verdicts = await parallel(
    checked.map(c => () =>
      agent(
        `Claim: ${c.claim}\nSource it rests on: ${c.source_url || 'none given'}\n` +
          `It will be used to answer: ${input.question} (item: ${item.id}).\n` +
          'Try to refute it. If you cannot verify it and cannot break it, answer refuted.',
        { label: `refute:${item.id}`, phase: 'Refute', agentType: 'founder-pipeline:claim-refuter', schema: VERDICT },
      )),
  )
  return {
    ...finding,
    item: item.id,
    // A skeptic that died counts as "not verified", never as "survived".
    verdicts: verdicts.map((v, i) => v || { claim: checked[i].claim, refuted: true, evidence: 'refuter returned nothing' }),
    unchecked: finding.claims.length - checked.length,
  }
}

const results = await pipeline(items, scout, refute)
const findings = results.map((r, i) => r || { item: items[i].id, failed: true, fields: [], claims: [], verdicts: [], unchecked: 0 })

const failed = findings.filter(f => f.failed).map(f => f.item)
const unchecked = findings.reduce((n, f) => n + f.unchecked, 0)
const surviving = findings.flatMap(f => f.verdicts.filter(v => !v.refuted).map(v => ({ item: f.item, claim: v.claim })))
const refuted = findings.flatMap(f => f.verdicts.filter(v => v.refuted).map(v => ({ item: f.item, claim: v.claim, evidence: v.evidence })))

// No silent caps: say what was dropped.
if (failed.length) log(`${failed.length} item(s) returned nothing: ${failed.join(', ')}`)
if (unchecked) log(`${unchecked} claim(s) beyond the per-item cap of ${maxClaims} were not sent to a skeptic`)

phase('Completeness')
const critic = await agent(
  `Question the sweep had to answer: ${input.question}\n` +
    `Items covered (${items.length}): ${items.map(i => i.id).join(', ')}\n` +
    `Items with no result: ${failed.join(', ') || 'none'}\n` +
    `Fields requested: ${fields.join(', ')}\n` +
    `Fields that came back NOT_FOUND: ${JSON.stringify(findings.flatMap(f => f.fields.filter(x => x.status === 'NOT_FOUND').map(x => `${f.item}:${x.name}`)))}\n` +
    `Claims that survived refutation: ${JSON.stringify(surviving)}\n` +
    `Claims refuted: ${refuted.length}. Claims never checked: ${unchecked}.\n` +
    'What is missing?',
  { label: 'completeness', agentType: 'founder-pipeline:completeness-critic', schema: GAPS },
)

return {
  question: input.question,
  findings,
  surviving,
  refuted,
  dropped: { failedItems: failed, uncheckedClaims: unchecked },
  // No critic verdict means the sweep is not complete.
  complete: Boolean(critic && critic.complete) && !failed.length && !unchecked,
  gaps: critic ? critic.gaps : [{ gap: 'completeness critic returned nothing', next_action: 're-run the critic' }],
}
