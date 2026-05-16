# Claude Global Workflow

## Product Development Pipeline

Every project follows 10 phases in order. Each phase requires explicit user confirmation before moving to the next. Never skip a phase.

```
[1] Requirements → [2] Planning → [3] Plan Report → [4] Epics & Stories → [5] Figma Design → [6] Tech Stack → [7] Build → [8] Test → [9] Deploy → [10] Report
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
       ├── plan.md                  ← created in Phase 2
       ├── plan-report.md           ← created in Phase 3
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

## Phase 2 — Planning

**Goal:** Think through the full solution before committing to stories or code.

Steps:
1. Based on the confirmed requirements, draft a structured plan covering:
   - Proposed solution approach (how the product will work at a high level)
   - Key technical decisions to make (platform, architecture, data flow)
   - Risks and open questions
   - Suggested epic breakdown (names only, no stories yet)
   - Rough effort estimate per epic (small / medium / large)
2. Write the plan to `.claude/plan.md`
3. Present the plan to the user and ask: "Does this plan look right? Any changes before we finalize it?"

**Do not proceed to Phase 3 until user confirms.**

---

## Phase 3 — Plan Report

**Goal:** Produce a clean, final plan document the user can reference throughout the project.

Steps:
1. Incorporate any changes from Phase 2 review
2. Write the final plan to `.claude/plan-report.md` with these sections:
   ```
   # Plan Report — <Project Name>

   ## Solution Overview
   - What we are building and how it works

   ## Epic Breakdown
   - Table: Epic | Description | Effort

   ## Key Decisions
   - Platform, architecture, tech choices to be confirmed in Phase 6

   ## Risks & Mitigations
   - Known risks and how we will handle them

   ## Out of Scope
   - What we are deliberately not building

   ## Success Criteria
   - How we will know the project is done
   ```
3. Show the final report to the user and ask: "Is this plan confirmed? We will now move to epics and stories."

**Do not proceed to Phase 4 until user confirms.**

---

## Phase 4 — Epics, User Stories, Acceptance Criteria & Edge Cases

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

**Do not proceed to Phase 5 until user confirms.**

---

## Phase 5 — Figma Design

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

**Do not proceed to Phase 6 until user confirms.**

Note: Figma MCP must be configured in `~/.claude/settings.json` with a valid personal access token.

---

## Phase 6 — Tech Stack Decision

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

**Do not proceed to Phase 7 until user confirms.**

---

## Phase 7 — Build

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

**Do not proceed to Phase 8 until all epics are complete and user confirms.**

---

## Phase 8 — Testing

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

**Do not proceed to Phase 9 until all tests pass and user confirms.**

---

## Phase 9 — Deploy to Hostinger VPS

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

## Phase 10 — Project Report

**Goal:** Generate a full written report of the completed project.

Trigger: Automatically after Phase 7 is confirmed complete.

Steps:
1. Generate `PROJECT-REPORT.md` in the project root with the following sections:

   ```
   # Project Report — <Project Name>
   
   ## Overview
   - One paragraph summary of what was built and why
   
   ## Timeline
   - Date started / date shipped
   - Total phases completed
   
   ## Requirements Summary
   - Problem statement
   - Target users
   - Core flows delivered
   - Items that were out of scope
   
   ## Epics & Stories
   - Table: Epic | Stories | Status
   - Total acceptance criteria written
   - Total edge cases covered
   
   ## Design
   - Figma file link
   - Number of screens/frames designed
   - Key design decisions
   
   ## Tech Stack
   - Framework, language, libraries used
   - Reasoning for choices
   
   ## Testing
   - Total tests written
   - Pass rate (X/Y)
   - Test types (unit / integration / E2E)
   
   ## Deployment
   - Platform (web / Android / iOS)
   - Build tool used
   - Live URL or store link
   - GitHub repo link
   
   ## Lessons Learned
   - What went well
   - What was challenging
   - What would be done differently
   
   ## Next Steps
   - Suggested improvements or features for v2
   ```

2. Push `PROJECT-REPORT.md` to GitHub
3. Tell the user: "Full project report saved to PROJECT-REPORT.md and pushed to GitHub."

---

## Rules

- **Always create a GitHub repo at the very start of a new project** — before any code is written
- Always read the project's `CLAUDE.md` and `.claude/` folder at the start of every session to understand the current phase
- Never implement anything before Phase 4 is confirmed
- Never deploy without Phase 6 tests passing
- Keep epic files updated as the single source of truth for what is done vs pending
- If the user asks "where are we?" summarize the current phase and what's pending
- Commit and push to GitHub after each completed phase

---

## Lessons Learned (Applied to All Future Projects)

These rules come from real mistakes made during the Smart Calculator project. Follow them every time.

### 📦 Dependencies
- **Always use `npx expo install <package>` — never `npm install`** for React Native / Expo projects
  - `npx expo install` automatically picks the SDK-compatible version
  - `npm install` installs the latest version which often breaks the build
  - Run `npx expo install` for every single package: reanimated, async-storage, etc.

### 🏗️ Build
- **Run a test EAS build at the end of Phase 5 (Build), not Phase 7 (Deploy)**
  - Catch build errors (missing babel plugins, Node version mismatches, broken deps) early
  - Command: `eas build --profile preview --platform android --non-interactive`
  - Fix all build errors before moving to Phase 6 (Testing)

### 🎨 Figma MCP
- **Set up the Figma MCP plugin before Phase 3 (Design) begins — not during it**
  - Steps to do at project start:
    1. Start WebSocket server: `~/.bun/bin/bun /usr/local/lib/node_modules/claude-talk-to-figma-mcp/dist/socket.js &`
    2. Open Figma Desktop → Plugins → Development → Claude Talk to Figma Plugin → Run → Connect
    3. Confirm green "Connected" status before entering Phase 3
  - If plugin code.js is missing: download from sonnylazuardi/cursor-talk-to-figma-mcp on GitHub
