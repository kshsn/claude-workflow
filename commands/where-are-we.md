---
name: where-are-we
description: Summarize the current project status — phase, epic progress, what's done and what's next.
---

1. Read project CLAUDE.md — get current phase, last completed epic, deployment status
2. List all files in .claude/epics/ and read their completion status ([x] vs [ ])
3. Read .claude/requirements.md for scope context (briefly)
4. Output a status summary:

   ```
   ## Project Status — [Project Name]
   Date: [today]

   **Current Phase:** [N] — [Phase Name]
   **Overall Progress:** [X/10 phases complete]
   **Deployment:** [IN PROGRESS / PRODUCTION / NOT STARTED]

   ## Epic Progress
   | Epic | Stories Total | Done | Status |
   |------|--------------|------|--------|
   | ...  | ...          | ...  | ...    |

   ## What's Done
   - [List completed phases and epics]

   ## What's Next
   1. [Immediate next action]
   2. [Then...]
   3. [Then...]
   ```

5. Ask: "Ready to continue? Type /phase-start to proceed."
