---
name: memory
description: Display the current project's memory from the cloud database — decisions, blockers, active work, key facts, and session log. Project is auto-detected from the current directory name.
argument-hint: [project-name (optional, defaults to current folder)]
---

Arguments: $ARGUMENTS

Steps:
1. Detect the project name:
   - If $ARGUMENTS is provided, use it as the project name
   - Otherwise use the current directory name

2. Run:
   ```bash
   python "C:/Users/Khaled/.claude/scripts/project-memory.py" read --project "<project-name>"
   ```
   On Mac/Linux: `python3 ~/.claude/scripts/project-memory.py read --project "<project-name>"`

3. Display the output grouped by section:
   - **Decisions** — choices made and why
   - **Active Work** — current phase, epic, or task
   - **Blockers** — waiting on someone or something
   - **Key Facts** — URLs, deadlines, limits, contacts
   - **Session Log** — what was done each session

4. After displaying, suggest:
   - `/remember <text>` to add a new entry
   - `/forget <keyword>` to remove something outdated
