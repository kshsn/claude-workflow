---
name: remember
description: Save a fact, decision, blocker, or note to the current project's cloud memory. Accessible from any device.
argument-hint: [text to remember]
---

Arguments: $ARGUMENTS

Steps:
1. Extract the text from $ARGUMENTS. If empty, ask: "What should I remember?"

2. Detect project name using this priority:
   - Check `CLAUDE.md` first heading in cwd
   - Run `git remote get-url origin` and extract repo name
   - Check `package.json` name field
   - Fall back to directory name (but never use the home folder name)

3. Classify into the best section:
   - **Decisions** — a choice was made ("decided to use X instead of Y because Z")
   - **Active Work** — current phase, epic, or task in progress
   - **Blockers** — something is waiting ("blocked on client Figma approval")
   - **Key Facts** — a URL, deadline, rate limit, contact, or constraint
   - **Session Log** — summary of what was accomplished today

4. Run:
   ```bash
   python "C:/Users/Khaled/.claude/scripts/project-memory.py" add \
     --project "<current-directory-name>" \
     --section "<Section>" \
     --entry "<text>"
   ```
   On Mac/Linux: use `python3` and `~/.claude/scripts/project-memory.py`

5. Confirm: "Remembered under [Section]: [text]"

**Examples:**
- `/remember decided not to use Redux — scope too small`  → Decisions
- `/remember blocked on Figma mockups from designer`  → Blockers
- `/remember staging URL is http://staging.example.com`  → Key Facts
- `/remember completed Phase 3 plan report today`  → Session Log
