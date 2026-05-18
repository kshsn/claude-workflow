---
name: project
description: Display the current project's cloud memory — decisions, blockers, active work, key facts, and session log.
argument-hint: [project-name (optional)]
---

Arguments: $ARGUMENTS

Steps:
1. Detect the project name using this priority order:
   - If $ARGUMENTS is provided → use it directly
   - Check for a `CLAUDE.md` in cwd → read the project name from the first `# ` heading
   - Run `git remote get-url origin` → extract repo name from the URL
   - Check for `package.json` → read the `name` field
   - Fall back to the current directory name

2. Run:
   ```bash
   python "C:/Users/Khaled/.claude/scripts/project-memory.py" read --project "<detected-name>"
   ```
   On Mac/Linux: `python3 ~/.claude/scripts/project-memory.py read --project "<detected-name>"`

3. Display the output clearly grouped by section:
   - **Decisions** — choices made and why
   - **Active Work** — current phase, epic, or task
   - **Blockers** — waiting on someone or something
   - **Key Facts** — URLs, deadlines, limits, contacts
   - **Session Log** — what was done each session

4. After displaying, suggest:
   - `/remember <text>` to add a new entry
   - `/forget <keyword>` to remove something outdated
