---
type: regex
pattern: '(paying customer|runway)[^\n]*\b(PASS|FAIL)\b|\b(PASS|FAIL)\b[^\n]*(paying customer|runway)'
flags: i
target: last_message
---
