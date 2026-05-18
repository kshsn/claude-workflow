---
name: forget
description: Remove an outdated or resolved entry from the current project's cloud memory by keyword.
argument-hint: [keyword to remove]
---

Arguments: $ARGUMENTS

Steps:
1. Extract the keyword from $ARGUMENTS. If empty, run `/memory` first so the user can pick the right keyword.

2. Detect project name (CLAUDE.md → git remote → package.json → folder name).

3. Run:
   ```bash
   python "C:/Users/Khaled/.claude/scripts/project-memory.py" forget \
     --project "<current-directory-name>" \
     --keyword "<keyword>"
   ```
   On Mac/Linux: use `python3` and `~/.claude/scripts/project-memory.py`

4. Report how many entries were removed.
   If 0 removed, show current memory with `/memory` so the user can find the right keyword.

**When to use:**
- Blocker is resolved → `/forget figma mockups`
- Decision was reversed → `/forget redux`
- Work item is done → `/forget phase 3`
- Outdated fact → `/forget staging url`
