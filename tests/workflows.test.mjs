// Runs the shipped workflow scripts against a mocked runner, so the orchestration
// logic is tested without spending a token. Run: node --test tests/
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const load = name => readFileSync(fileURLToPath(new URL(`../plugins/founder-pipeline/workflows/${name}.js`, import.meta.url)), 'utf8')

// Same contract as the real runner: pipeline() threads each item through the stages and a
// throwing stage drops the item to null; parallel() resolves a throwing thunk to null.
function runner(agentImpl) {
  const calls = []
  const logs = []
  const agent = async (prompt, opts = {}) => { calls.push({ prompt, ...opts }); return agentImpl(prompt, opts) }
  const parallel = thunks => Promise.all(thunks.map(t => t().catch(() => null)))
  const pipeline = (items, ...stages) => Promise.all(items.map(async (item, i) => {
    let value = item
    for (const stage of stages) {
      try { value = await stage(value, item, i) } catch { return null }
    }
    return value
  }))
  return { calls, logs, agent, parallel, pipeline, phase: () => {}, log: m => logs.push(m) }
}

async function run(name, args, agentImpl) {
  const src = load(name).replace('export const meta', 'const meta')
  const r = runner(agentImpl)
  const fn = new AsyncFunction('agent', 'parallel', 'pipeline', 'phase', 'log', 'args', src)
  const result = await fn(r.agent, r.parallel, r.pipeline, r.phase, r.log, args)
  return { result, calls: r.calls, logs: r.logs }
}

const finding = (item, claims) => ({ item, fields: [{ name: 'size', value: '40', source_url: 'https://e.example/a', accessed: '2026-11-13', status: 'VERIFIED' }], claims })

test('meta block is a pure literal with a name and description in both scripts', () => {
  for (const name of ['gather-verify', 'judge-panel']) {
    const m = load(name).match(/^export const meta = (\{[\s\S]*?\n\})\n/)
    assert.ok(m, `${name}: meta must be the first statement`)
    const meta = new Function(`return ${m[1]}`)()
    assert.equal(meta.name, name)
    assert.ok(meta.description.length > 20)
    assert.ok(!/\$\{|\.\.\./.test(m[1]), `${name}: meta must not interpolate or spread`)
  }
})

test('gather-verify: one scout per item, one skeptic per claim, one completeness critic', async () => {
  const { result, calls } = await run('gather-verify', { question: 'Do they have the pain?', fields: ['size'], items: ['acme', { id: 'globex', context: 'B2B' }] },
    (prompt, o) => {
      if (o.agentType.endsWith('evidence-scout')) return finding(o.label, [{ claim: `${o.label} hires fast`, source_url: 'https://e.example/b' }])
      if (o.agentType.endsWith('claim-refuter')) return { claim: 'x', refuted: prompt.includes('scout:acme'), evidence: 'checked' }
      return { complete: true, gaps: [] }
    })
  const by = t => calls.filter(c => c.agentType === `founder-pipeline:${t}`)
  assert.equal(by('evidence-scout').length, 2)
  assert.equal(by('claim-refuter').length, 2)
  assert.equal(by('completeness-critic').length, 1)
  assert.ok(calls.every(c => c.schema && !c.model), 'every agent returns structured output; tiers come from agent definitions, not the script')
  assert.equal(result.refuted.length, 1)
  assert.equal(result.surviving.length, 1)
  assert.equal(result.surviving[0].item, 'globex')
  assert.equal(result.complete, true)
})

test('gather-verify: a skeptic that dies counts as refuted, never as survived', async () => {
  const { result } = await run('gather-verify', { question: 'q', fields: ['f'], items: ['a'] }, (p, o) => {
    if (o.agentType.endsWith('evidence-scout')) return finding('a', [{ claim: 'c1' }])
    if (o.agentType.endsWith('claim-refuter')) return null
    return { complete: true, gaps: [] }
  })
  assert.equal(result.surviving.length, 0)
  assert.equal(result.refuted.length, 1)
})

test('gather-verify: a dead scout and capped claims are reported, and the sweep is not complete', async () => {
  const { result, logs } = await run('gather-verify', { question: 'q', fields: ['f'], items: ['a', 'b'], maxClaimsPerItem: 1 }, (p, o) => {
    if (o.agentType.endsWith('evidence-scout')) return o.label === 'scout:b' ? null : finding('a', [{ claim: 'c1' }, { claim: 'c2' }])
    if (o.agentType.endsWith('claim-refuter')) return { claim: 'c1', refuted: false, evidence: 'ok' }
    return { complete: true, gaps: [] }
  })
  assert.deepEqual(result.dropped, { failedItems: ['b'], uncheckedClaims: 1 })
  assert.equal(result.complete, false, 'a critic saying complete cannot override dropped work')
  assert.equal(logs.length, 2, 'both caps are logged, none is silent')
})

test('gather-verify: a missing completeness verdict means not complete', async () => {
  const { result } = await run('gather-verify', { question: 'q', fields: ['f'], items: ['a'] }, (p, o) =>
    o.agentType.endsWith('evidence-scout') ? finding('a', []) : null)
  assert.equal(result.complete, false)
  assert.equal(result.gaps.length, 1)
})

test('gather-verify and judge-panel refuse to run without their arguments', async () => {
  await assert.rejects(run('gather-verify', { question: 'q', items: ['a'] }, () => null), /needs args/)
  await assert.rejects(run('gather-verify', undefined, () => null), /needs args/)
  await assert.rejects(run('judge-panel', { artifactPath: 'x.md', criteria: [] }, () => null), /needs args/)
})

const verdicts = (n, pass = true) => Array.from({ length: n }, (_, i) => ({ criterion: `c${i + 1}`, pass, evidence: 'line 3' }))

test('judge-panel: one blind critic per framing, and the gate passes only if every framing passes', async () => {
  const args = { artifactPath: 'P2-Viability.S4-Validation.md', criteria: ['a', 'b'], framings: ['refute the profit case', 'refute the focus case'] }
  const pass = await run('judge-panel', args, () => ({ verdicts: verdicts(2), blocking: [], gate: 'PASS', score: 8 }))
  assert.equal(pass.calls.length, 2)
  assert.ok(pass.calls.every(c => c.agentType === 'founder-pipeline:gate-critic'))
  assert.ok(!pass.calls[0].prompt.includes('focus case'), 'a critic never sees the other framing')
  assert.equal(pass.result.gate, 'PASS')

  const split = await run('judge-panel', args, p => p.includes('profit')
    ? { verdicts: verdicts(2), blocking: [], gate: 'PASS', score: 9 }
    : { verdicts: verdicts(2, false), blocking: [], gate: 'FAIL', score: 4 })
  assert.equal(split.result.gate, 'FAIL', 'a panel never averages')
})

test('judge-panel: the gate is computed from the verdicts, not taken from the critic summary', async () => {
  const args = { artifactPath: 'x.md', criteria: ['a', 'b', 'c'] }
  const lying = await run('judge-panel', args, () => ({ verdicts: [...verdicts(2), { criterion: 'c3', pass: false, evidence: 'none' }], blocking: [], gate: 'PASS', score: 9 }))
  assert.equal(lying.result.gate, 'FAIL', 'a failed criterion fails the gate even if the critic wrote PASS')

  const partial = await run('judge-panel', args, () => ({ verdicts: verdicts(2), blocking: [], gate: 'PASS', score: 9 }))
  assert.equal(partial.result.gate, 'FAIL', 'skipping a criterion fails the gate')

  const blocked = await run('judge-panel', args, () => ({ verdicts: verdicts(3), blocking: ['source does not exist'], gate: 'PASS', score: 9 }))
  assert.equal(blocked.result.gate, 'FAIL', 'a blocking finding fails the gate')

  const dead = await run('judge-panel', args, () => null)
  assert.equal(dead.result.gate, 'FAIL', 'a critic that returns nothing fails the gate')
})
