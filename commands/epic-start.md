---
name: epic-start
description: Start a new epic. Creates the epic file from template, defines stories, begins implementation.
argument-hint: [epic-number] [epic-slug]
---

Arguments: $ARGUMENTS (example: "001 auth" or "002 dashboard")

1. Parse epic number and slug from $ARGUMENTS
2. Read .claude/requirements.md and .claude/plan-report.md for context
3. Copy ~/.claude/templates/epic.md → .claude/epics/epic-{number}-{slug}.md
4. Fill in: Goal (one sentence), 3–5 user stories with acceptance criteria + edge cases
5. Show the epic to the user and ask: "Does this epic look right? Confirm to start building."
6. On confirm: implement US-001 first using vertical slices (DB + API + UI together)
7. After each story: mark [x] in epic file, run type check + linter
8. After all stories complete:
   - Commit epic file: `git add .claude/epics/epic-{number}-{slug}.md && git commit -m "epic: complete epic {number} {slug}"`
   - Update project CLAUDE.md: set "Last Completed Epic"
   - Ask: "Epic {number} done. Ready for the next epic?"
