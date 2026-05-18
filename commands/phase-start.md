---
name: phase-start
description: Start the next project phase. Reads CLAUDE.md, confirms phase number, executes all phase steps.
argument-hint: [phase-number]
---

1. Read the project CLAUDE.md — find the current phase from the Phase Progress checklist
2. If $ARGUMENTS given, use that phase number; otherwise use the next unchecked phase
3. Load the relevant phase doc:
   - Phases 1–3 → read ~/.claude/docs/phases-1-3.md
   - Phases 4–6 → read ~/.claude/docs/phases-4-6.md
   - Phases 7–10 → read ~/.claude/docs/phases-7-10.md
4. Announce: "Starting Phase [N] — [Phase Name]"
5. Execute every step in that phase in order
6. At the end, ask: "Phase [N] complete. Confirm to mark it done and move to Phase [N+1]?"
7. When confirmed:
   - Mark phase [x] in project CLAUDE.md
   - Update "Current Phase" field
   - Commit: `git add CLAUDE.md && git commit -m "phase: complete phase [N] — [name]"`
