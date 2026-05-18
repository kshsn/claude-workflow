---
name: lesson
description: Log a lesson learned to the persistent lesson database. Call this immediately after fixing a mistake or being corrected.
argument-hint: [lesson description]
---

Arguments: $ARGUMENTS

Steps:
1. Extract the lesson text from $ARGUMENTS (or ask if empty)
2. Classify into one category:
   - `dependencies` — package management (npm, expo, pip, versions)
   - `build`        — build/compile/bundler errors
   - `hooks`        — Claude Code hook issues
   - `testing`      — test writing, running, or flaky tests
   - `deployment`   — deploy, server, PM2, rsync issues
   - `git`          — git workflow, commits, branches
   - `security`     — secrets, auth, OWASP patterns
   - `design`       — Figma, UI, layout decisions
   - `workflow`     — phase process, planning, sequencing
   - `general`      — anything else
3. If the "why" (root cause) isn't obvious from the description, ask one question: "Why did this happen?"
4. Run:
   ```bash
   python "C:/Users/Khaled/.claude/scripts/log-lesson.py" \
     --category "<category>" \
     --lesson "<lesson text>" \
     --why "<root cause>" \
     --trigger "auto"
   ```
5. Also add an entry to `~/.claude/docs/lessons-learned.md` under the matching category section
6. Confirm: "Lesson logged under [category]: [lesson]"

Example triggers to use /lesson proactively (without being asked):
- You fix a bug you introduced
- You rewrite something you wrote wrong the first time
- The user says "no", "wrong", "don't", "actually", or similar
- A hook blocks something unexpectedly
- A build/test fails due to a pattern you should have known
