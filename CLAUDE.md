# Claude Global Workflow

## Product Development Pipeline

Every project follows 7 phases in order. Each phase requires explicit user confirmation before moving to the next. Never skip a phase.

```
[1] Requirements → [2] Epics & Stories → [3] Figma Design → [4] Tech Stack → [5] Build → [6] Test → [7] Deploy
```

---

## Starting a New Project

When the user says "start a new project", "new project", or describes an idea for the first time:

1. Ask for the project name if not given
2. **Create a GitHub repository immediately** (before writing any code):
   ```bash
   mkdir <project-name> && cd <project-name> && git init
   gh repo create <project-name> --public --source=. --remote=origin
   ```
   All work happens inside this repo from the start.
3. Create this folder structure in the current directory:
   ```
   <project-name>/
   ├── CLAUDE.md                    ← copy from ~/.claude/templates/project-CLAUDE.md
   └── .claude/
       ├── requirements.md          ← copy from ~/.claude/templates/requirements.md
       ├── epics/                   ← empty folder
       ├── design/
       │   ├── figma.md
       │   └── decisions.md
       ├── tech-stack.md
       └── deployment/
           └── server.md            ← copy from ~/.claude/templates/server.md
   ```
3. Enter Phase 1 immediately

---

## Phase 1 — Requirements Capture

**Goal:** Turn a rough idea into a structured requirements document.

Steps:
1. Ask these questions if not already answered:
   - Who are the target users?
   - What is the core problem being solved?
   - What are the 3–5 most important actions users need to do?
   - What is explicitly out of scope?
   - Any constraints (deadline, budget, platform)?
2. Write structured output to `.claude/requirements.md` using the template
3. Show the user a summary and ask: "Does this capture your requirements? Confirm to move to Phase 2."

**Do not proceed to Phase 2 until user confirms.**

---

## Phase 2 — Epics, User Stories, Acceptance Criteria & Edge Cases

**Goal:** Break requirements into well-defined epics and stories.

Steps:
1. Group features into 2–6 epics
2. For each epic, create `.claude/epics/epic-NNN-<slug>.md` using the template at `~/.claude/templates/epic.md`
3. Each story must have:
   - User story format: "As a [user type], I want to [action] so that [value]"
   - At least 3 acceptance criteria (Given/When/Then format)
   - At least 3 edge cases
4. Show a summary table of all epics and story counts
5. Ask: "Do the epics and stories look complete? Confirm or tell me what to change."

**Do not proceed to Phase 3 until user confirms.**

---

## Phase 3 — Figma Design

**Goal:** Create or review designs for every story.

Steps:
1. Ask: "Do you have an existing Figma file? If yes, share the URL. If no, I'll create one."
2. Use the Figma MCP to:
   - **Existing file:** Read the file, map frames to stories, note gaps
   - **New file:** Create frames named after each epic and key stories
3. Write frame inventory and links to `.claude/design/figma.md`
4. Walk through each screen with the user in chat
5. For each confirmed screen, add a line to `.claude/design/decisions.md`
6. Ask: "Are all designs confirmed? Confirm to move to Phase 4."

**Do not proceed to Phase 4 until user confirms.**

Note: Figma MCP must be configured in `~/.claude/settings.json` with a valid personal access token.

---

## Phase 4 — Tech Stack Decision

**Goal:** Choose the right technology for this project.

Default recommendations:
- **Full-stack web:** Next.js 14 + TypeScript + PostgreSQL + Prisma + Tailwind CSS
- **Mobile:** React Native + Expo + TypeScript + NativeWind
- **Backend API only:** Node.js + Fastify + TypeScript + PostgreSQL + Prisma
- **Backend (large/complex):** NestJS + TypeScript + PostgreSQL + Prisma

Steps:
1. Recommend a stack based on project type with brief rationale
2. List all key dependencies and tooling
3. Write the decision to `.claude/tech-stack.md`
4. Ask: "Does this stack work for you? Confirm or override any part of it."

**Do not proceed to Phase 5 until user confirms.**

---

## Phase 5 — Build

**Goal:** Implement all epics story by story.

Steps:
1. Scaffold the project with the chosen framework
2. Work through epics in order (epic-001 first)
3. Within each epic, implement stories in order (US-001, US-002, ...)
4. After each story is complete:
   - Mark it `[x]` in the epic file
   - Run type check and linter
5. After each epic is complete:
   - Update `CLAUDE.md` current phase and last completed epic
6. Ask: "Epic [N] is done. Ready to continue to the next epic?"

**Do not proceed to Phase 6 until all epics are complete and user confirms.**

---

## Phase 6 — Testing

**Goal:** Verify all functionality before deploying.

Steps:
1. Write unit tests for all business logic functions
2. Write integration tests for all API endpoints
3. Write E2E smoke tests for the top 3 critical user flows:
   - Web: Playwright
   - Mobile: Detox or Maestro
4. Run the full test suite
5. Fix any failures before continuing
6. Report results: X/Y tests passing
7. Ask: "All tests pass. Ready to deploy?"

**Do not proceed to Phase 7 until all tests pass and user confirms.**

---

## Phase 7 — Deploy to Hostinger VPS

**Goal:** Ship to production.

Steps:
1. Read `.claude/deployment/server.md` for host, user, app path, PM2 process name
2. Build the production bundle
3. For full-stack/web:
   ```bash
   rsync -avz --exclude node_modules --exclude .git ./dist user@host:/var/www/<project>
   ssh user@host "cd /var/www/<project> && npm install --production && pm2 restart <process-name>"
   ```
4. For mobile: run `eas build --platform all` and submit to stores
5. Verify with a health-check HTTP request to the production URL
6. Update `CLAUDE.md` status to `PRODUCTION` with deploy date
7. Tell the user: "Project is live at [URL]."

---

## Rules

- **Always create a GitHub repo at the very start of a new project** — before any code is written
- Always read the project's `CLAUDE.md` and `.claude/` folder at the start of every session to understand the current phase
- Never implement anything before Phase 4 is confirmed
- Never deploy without Phase 6 tests passing
- Keep epic files updated as the single source of truth for what is done vs pending
- If the user asks "where are we?" summarize the current phase and what's pending
- Commit and push to GitHub after each completed phase
