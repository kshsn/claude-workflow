---
name: recall
description: Fetch and display all lessons learned from the VPS database. Works from any device. Optionally filter by category.
argument-hint: [category] [--limit N]
---

Arguments: $ARGUMENTS

Steps:
1. Run the recall script (VPS first, local JSONL fallback):
   ```bash
   python "C:/Users/Khaled/.claude/scripts/recall-lessons.py" $ARGUMENTS
   ```
   On Mac/Linux: `python3 ~/.claude/scripts/recall-lessons.py $ARGUMENTS`

2. Read the output and present lessons grouped by category in a clear summary.

3. After displaying, offer one of:
   - `/lesson <text>` — log a new lesson now
   - `/learning-report` — full analysis with trends and recommendations

**Categories you can filter by:**
`dependencies` | `build` | `hooks` | `testing` | `deployment` | `git` | `security` | `design` | `workflow` | `general`

**Examples:**
- `/recall` — all lessons from VPS
- `/recall git` — only git lessons
- `/recall hooks --limit 5` — last 5 hook lessons
