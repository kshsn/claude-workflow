# Phases 1–3: Discovery & Planning

---

## Phase 1 — Requirements Capture
**Goal:** Turn a rough idea into a structured requirements document.

Steps:
1. Ask these questions if not already answered:
   - Who are the target users?
   - What is the core problem being solved?
   - What are the 3–5 most important user actions?
   - What is explicitly out of scope?
   - Any constraints (deadline, budget, platform)?
2. Write structured output to `.claude/requirements.md` using `~/.claude/templates/requirements.md`
3. Show summary and ask: "Does this capture your requirements? Confirm to move to Phase 2."

> **Gate:** Do not proceed to Phase 2 until user confirms.

---

## Phase 2 — Planning
**Goal:** Think through the full solution before committing to stories or code.

Steps:
1. Draft a structured plan covering:
   - Proposed solution approach (how the product works at a high level)
   - Key technical decisions (platform, architecture, data flow)
   - Risks and open questions
   - Suggested epic breakdown (names only, no stories yet)
   - Rough effort estimate per epic (small / medium / large)
2. Write to `.claude/plan.md`
3. Present and ask: "Does this plan look right? Any changes before we finalize it?"

> **Gate:** Do not proceed to Phase 3 until user confirms.

---

## Phase 3 — Plan Report
**Goal:** Produce a clean, final plan document the user can reference throughout the project.

Steps:
1. Incorporate any changes from Phase 2 review
2. Write final plan to `.claude/plan-report.md` with these sections:
   ```
   # Plan Report — <Project Name>
   ## Solution Overview
   ## Epic Breakdown       ← Table: Epic | Description | Effort
   ## Key Decisions
   ## Risks & Mitigations
   ## Out of Scope
   ## Success Criteria
   ```
3. Ask: "Is this plan confirmed? We will now move to epics and stories."

> **Gate:** Do not proceed to Phase 4 until user confirms.
