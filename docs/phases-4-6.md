# Phases 4–6: Design & Tech Stack

---

## Phase 4 — Epics, User Stories, Acceptance Criteria & Edge Cases
**Goal:** Break requirements into well-defined epics and stories.

Steps:
1. Group features into 2–6 epics
2. For each epic, create `.claude/epics/epic-NNN-<slug>.md` using `~/.claude/templates/epic.md`
3. Each story must have:
   - User story: "As a [user type], I want to [action] so that [value]"
   - At least 3 acceptance criteria (Given / When / Then format)
   - At least 3 edge cases
4. Show a summary table of all epics and story counts
5. Ask: "Do the epics and stories look complete? Confirm or tell me what to change."

> **Gate:** Do not proceed to Phase 5 until user confirms.

---

## Phase 5 — Figma Design
**Goal:** Create or review designs for every story.

**Pre-requisite:** Figma MCP must be running — see `~/.claude/docs/lessons-learned.md` for setup.

Steps:
1. Ask: "Do you have an existing Figma file? If yes, share the URL. If no, I'll create one."
2. Use Figma MCP to:
   - **Existing file:** Read the file, map frames to stories, note gaps
   - **New file:** Create frames named after each epic and key stories
3. Write frame inventory and links to `.claude/design/figma.md`
4. Walk through each screen with the user in chat
5. For each confirmed screen, add a line to `.claude/design/decisions.md`
6. Ask: "Are all designs confirmed? Confirm to move to Phase 6."

> **Gate:** Do not proceed to Phase 6 until user confirms.

---

## Phase 6 — Tech Stack Decision
**Goal:** Choose the right technology for this specific project.

Steps:
1. Recommend a stack based on project type (see global CLAUDE.md for defaults)
2. List all key dependencies and tooling with version numbers
3. Write the decision to `.claude/tech-stack.md`:
   ```
   # Tech Stack — <Project Name>
   ## Framework & Language
   ## Database & ORM
   ## Styling
   ## Testing Tools
   ## Deployment Platform
   ## Reasoning
   ```
4. Ask: "Does this stack work for you? Confirm or override any part of it."

> **Gate:** Do not proceed to Phase 7 until user confirms.
