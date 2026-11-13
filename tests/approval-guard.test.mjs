// Run: node --test tests/
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { decide } from '../plugins/founder-pipeline/hooks/approval-guard.mjs'

const SCRIPT = fileURLToPath(new URL('../plugins/founder-pipeline/hooks/approval-guard.mjs', import.meta.url))
const HEADER = '| Step | Name | Status | Updated | CRITICAL | Def-of-success | Note |\n|---|---|---|---|---|---|---|\n'
const row = status => `| P1.S2 | Problem | ${status} | 2026-11-13 | 8/10 | 6/6 | ok |\n`
const pipelineFile = status => HEADER + row(status)
const edit = (file_path, old_string, new_string) => ({ tool_name: 'Edit', tool_input: { file_path, old_string, new_string } })
const write = (file_path, content) => ({ tool_name: 'Write', tool_input: { file_path, content } })
const asks = d => d?.hookSpecificOutput?.permissionDecision === 'ask'

test('asks when an Edit flips a row to approved', () => {
  const d = decide(edit('/s/PROGRESS.md', row('awaiting approval'), row('approved')), () => pipelineFile('awaiting approval'))
  assert.ok(asks(d))
  assert.equal(d.hookSpecificOutput.hookEventName, 'PreToolUse')
})

test('asks when a Write adds an approved row to an existing pipeline file', () => {
  const d = decide(write('/s/PROGRESS.md', pipelineFile('approved')), () => pipelineFile('awaiting approval'))
  assert.ok(asks(d))
})

test('asks when a brand-new PROGRESS.md is written already approved', () => {
  assert.ok(asks(decide(write('/s/PROGRESS.md', pipelineFile('approved')), () => '')))
})

test('stays silent for every transition that is not an approval', () => {
  for (const [from, to] of [['pending', 'in progress'], ['in progress', 'awaiting approval'], ['awaiting approval', 'skipped'], ['in progress', 'killed']]) {
    assert.equal(decide(edit('/s/PROGRESS.md', row(from), row(to)), () => pipelineFile(from)), null, `${from} -> ${to}`)
  }
})

test('stays silent when an approved row is rewound or merely rewritten', () => {
  assert.equal(decide(edit('/s/PROGRESS.md', row('approved'), row('in progress')), () => pipelineFile('approved')), null)
  assert.equal(decide(edit('/s/PROGRESS.md', row('approved'), row('approved').replace('ok', 'note fixed')), () => pipelineFile('approved')), null)
})

test('does not treat "awaiting approval" or prose mentioning approved as an approval', () => {
  const d = decide(edit('/s/PROGRESS.md', row('in progress'), row('awaiting approval')), () => pipelineFile('in progress'))
  assert.equal(d, null)
  const prose = decide(edit('/s/PROGRESS.md', 'x', 'only an approved row means approved'), () => pipelineFile('pending'))
  assert.equal(prose, null)
})

test('ignores other files, other tools, and a PROGRESS.md that is not the pipeline format', () => {
  assert.equal(decide(edit('/s/brief.md', 'a', '| approved |'), () => pipelineFile('pending')), null)
  assert.equal(decide({ tool_name: 'Bash', tool_input: { command: 'echo "| approved |" > PROGRESS.md' } }), null)
  assert.equal(decide(write('/other/PROGRESS.md', '| task | approved |\n'), () => '| task | status |\n'), null)
})

test('fails open: malformed stdin exits 0 with no output', () => {
  for (const stdin of ['', 'not json', '{"tool_name":"Edit"}', 'null']) {
    const r = spawnSync('node', [SCRIPT], { input: stdin, encoding: 'utf8' })
    assert.equal(r.status, 0, JSON.stringify(stdin))
    assert.equal(r.stdout, '', JSON.stringify(stdin))
  }
})

test('end to end: the script prints an ask decision as JSON on stdout', () => {
  const event = write('/nonexistent/PROGRESS.md', pipelineFile('approved'))
  const r = spawnSync('node', [SCRIPT], { input: JSON.stringify(event), encoding: 'utf8' })
  assert.equal(r.status, 0)
  assert.ok(asks(JSON.parse(r.stdout)))
})
