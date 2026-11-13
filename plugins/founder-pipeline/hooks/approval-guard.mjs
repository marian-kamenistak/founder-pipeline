#!/usr/bin/env node
// approval-guard — the pipeline's one rule that prose cannot enforce.
//
// The founder skill says a step is `approved` only when the owner signs it off.
// This PreToolUse hook makes that true in code: any Write or Edit that adds an
// `approved` row to a founder-pipeline PROGRESS.md, and any shell command that
// writes one, is turned into a permission prompt, so a human has to click before the row lands. In an unattended run
// nobody can click, which is the intended result: unattended steps stay at
// `awaiting approval` until the owner reviews them.
//
// It only ever asks. It never denies, and on any error it stays silent and lets
// the tool call through, so a bug here cannot block unrelated work.

import { readFileSync, existsSync } from 'node:fs'
import { basename } from 'node:path'

const APPROVED_ROW = /\|\s*approved\s*\|/gi
const PIPELINE_MARKER = 'Def-of-success' // column header of the pipeline's PROGRESS.md

const count = text => (String(text || '').match(APPROVED_ROW) || []).length

// A shell command that writes (redirect, in-place edit, tee, a script) and mentions both the
// state file and the word. Best effort: it reads the command text, it cannot see what a script does.
const SHELL_WRITE = /(>>?|\bsed\b[^|;]*\s-i|\bperl\b[^|;]*\s-[a-z]*i|\btee\b|\bpython3?\b|\bnode\b|\bawk\b[^|;]*-i|\bmv\b|\bcp\b)/

const ASK = reason => ({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: reason } })
const REASON =
  'founder-pipeline: this marks a step `approved` in PROGRESS.md. ' +
  'Only the owner approves a step. Allow it only if you have reviewed the step and its critic verdict.'

export function decide(event, readFile = p => (existsSync(p) ? readFileSync(p, 'utf8') : '')) {
  const tool = event?.tool_name
  const input = event?.tool_input || {}
  if (tool === 'Bash') {
    const cmd = String(input.command || '')
    return /PROGRESS\.md/.test(cmd) && /\bapproved\b/i.test(cmd) && SHELL_WRITE.test(cmd) ? ASK(REASON) : null
  }
  if (tool !== 'Write' && tool !== 'Edit') return null
  if (!input.file_path || basename(input.file_path) !== 'PROGRESS.md') return null

  const onDisk = readFile(input.file_path)
  const before = tool === 'Write' ? onDisk : input.old_string
  const after = tool === 'Write' ? input.content : input.new_string

  // Only guard the pipeline's own state file, not any file that happens to share the name.
  if (!`${onDisk}\n${after || ''}`.includes(PIPELINE_MARKER)) return null
  if (count(after) <= count(before)) return null

  return ASK(REASON)
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const decision = decide(JSON.parse(readFileSync(0, 'utf8')))
    if (decision) process.stdout.write(JSON.stringify(decision))
  } catch {
    // Fail open: malformed input or an unreadable file must never block a tool call.
  }
  process.exit(0)
}
