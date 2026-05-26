# Claude Global Workflow — CTO Pipeline

## Product Development Pipeline (Agile)

Every project follows 10 phases in strict order. Each phase ends with:
1. A phase report saved to `.claude/reports/phase-N-report.md`
2. Commit + push to GitHub
3. Sync artifacts to the VPS server (staging path)

Each phase requires explicit user confirmation before moving to the next. Never skip a phase.

```
[1] Market Research → [2] Plan & Requirements → [3] Epics & Stories (Jira)
→ [4] GitHub Repo + Tech Stack → [5] Figma Design (UI/UX Agent)
→ [6] Development (Agile Sprints) → [7] Testing → [8] Deploy to Server
→ [9] Server Testing → [10] Final Report
```

---

## Agile Methodology Rules (Apply to All Phases)

- All work is tracked in **Jira** via MCP — every task, bug, and story has a Jira issue
- Development (Phase 6) runs in **2-week sprints** with sprint planning, daily standups (summary), and sprint review
- Stories have **story points** (Fibonacci: 1, 2, 3, 5, 8, 13)
- Priority uses **MoSCoW**: Must Have, Should Have, Could Have, Won't Have
- Branching: `feature/epic-NNN`, `fix/issue-title`, `release/vX.X` — never commit to `main`
- All PRs require a description referencing the Jira story key (e.g. `PROJ-42`)
- Every sprint ends with a sprint report saved to `.claude/reports/sprint-N-report.md`

---

## End-of-Phase Protocol (Every Phase)

Run this at the end of EVERY phase before asking the user to confirm:

```bash
# 1. Write phase report
# Save to .claude/reports/phase-N-report.md

# 2. Commit and push to GitHub
git add -A
git commit -m "phase N complete: <phase name>"
git push origin main

# 3. Sync to VPS server (staging)
# Read server config from .claude/deployment/server.md first
rsync -avz --exclude node_modules --exclude .git \
  ./ user@host:/var/www/<project>-staging/
```

---

## Starting a New Project

When the user says "start a new project", "new project", or `/cto <project-name>`:

1. Ask for the project name if not given
2. **Do NOT create the GitHub repo yet** — that happens in Phase 4
3. Create this local folder structure immediately:
   ```
   <project-name>/
   ├── CLAUDE.md                        ← copy from ~/.claude/templates/project-CLAUDE.md
   └── .claude/
       ├── reports/                     ← phase and sprint reports go here
       ├── requirements.md              ← Phase 2
       ├── plan.md                      ← Phase 2
       ├── plan-report.md               ← Phase 2
       ├── market-research.md           ← Phase 1
       ├── epics/                       ← Phase 3 local copies
       ├── jira.md                      ← Phase 3 Jira project key + issue links
       ├── design/
       │   ├── figma.md                 ← Phase 5
       │   └── decisions.md            ← Phase 5
       ├── tech-stack.md               ← Phase 4
       └── deployment/
           └── server.md               ← copy from ~/.claude/templates/server.md
   ```
4. Enter Phase 1 immediately

---

## Phase 1 — Market Research

**Goal:** Validate the market before committing to requirements or code.

**Agile context:** This is the discovery sprint. Output feeds directly into Phase 2 backlog.

Steps:
1. Ask the user for a one-line product idea and target audience if not already provided
2. Research and document the following (use web search + user input):
   - **Problem Statement:** What pain are we solving? Who feels it most?
   - **Target Market:** Primary users, secondary users, market size estimate (TAM/SAM/SOM)
   - **Competitor Analysis:** 3–5 competitors — what they do, pricing, strengths, gaps
   - **Differentiation:** How is this product different or better?
   - **Market Risks:** Timing, regulatory, adoption risks
   - **Opportunity Score:** Rate the opportunity 1–10 with reasoning
3. Write findings to `.claude/market-research.md`
4. Generate **Phase 1 Report** → `.claude/reports/phase-1-report.md`:
   ```
   # Phase 1 Report — Market Research
   ## Summary
   ## Competitors Analyzed
   ## Key Opportunity
   ## Risks Identified
   ## Go / No-Go Recommendation
   ```
5. Run end-of-phase protocol (report → git commit → rsync)
6. Present findings and ask: "Market research complete. Do you want to proceed to Phase 2 (Requirements)?"

**Do not proceed to Phase 2 until user confirms.**

---

## Phase 2 — Plan & Requirements

**Goal:** Define exactly what we're building and produce a confirmed plan.

**Agile context:** This populates the product backlog at a high level. Sprints come in Phase 6.

Steps:
1. Ask focused questions (max 3 at a time) until you have answers to:
   - Who are the target users? (from Phase 1)
   - What are the 3–5 core user flows?
   - What is explicitly out of scope?
   - What are the constraints (deadline, budget, platform)?
   - What does success look like (KPIs)?
2. Write to `.claude/requirements.md` using the requirements template
3. Draft a plan covering:
   - Solution approach (how the product works at high level)
   - Architecture overview (frontend, backend, DB, integrations)
   - Suggested epic breakdown (names only — stories come in Phase 3)
   - Effort estimate per epic (S/M/L)
   - Risks and mitigations
4. Write plan to `.claude/plan.md`
5. Write final plan report to `.claude/plan-report.md`:
   ```
   # Plan Report — <Project Name>
   ## Solution Overview
   ## Epic Breakdown (Table: Epic | Description | Effort | Priority)
   ## Architecture Overview
   ## Key Decisions
   ## Risks & Mitigations
   ## Out of Scope
   ## Success Criteria (KPIs)
   ```
6. Generate **Phase 2 Report** → `.claude/reports/phase-2-report.md`
7. Run end-of-phase protocol
8. Ask: "Plan confirmed? Shall we move to Phase 3 and create all epics and stories in Jira?"

**Do not proceed to Phase 3 until user confirms.**

---

## Phase 3 — Epics & User Stories (Jira via MCP)

**Goal:** Break the plan into Jira epics and stories with full acceptance criteria. This is the official sprint backlog.

**Agile context:** This creates the product backlog in Jira. Stories are prioritized MoSCoW and estimated in story points.

Steps:
1. **Create Jira project** via MCP:
   - Use `createJiraIssue` or check `getVisibleJiraProjects` for an existing project
   - Record the Jira project key in `.claude/jira.md`
2. **Create Epics in Jira** (2–6 epics based on plan):
   - Each epic: name, description, priority, target sprint
   - Record Jira epic key in `.claude/jira.md`
3. **Create User Stories under each epic** in Jira:
   - Format: "As a [user type], I want to [action] so that [value]"
   - Each story must have:
     - At least 3 acceptance criteria (Given/When/Then)
     - At least 3 edge cases in the description
     - Story points (Fibonacci)
     - MoSCoW priority label
     - Assignee: leave unassigned for now
   - Use `createJiraIssue` with `issuetype: Story`, parent = epic key
4. **Create local epic files** at `.claude/epics/epic-NNN-<slug>.md` using the template at `~/.claude/templates/epic.md` — include the Jira story key on each story
5. Write full Jira index (project key, all epic keys, story keys) to `.claude/jira.md`
6. Show a summary table: Epic | Stories | Total Points | Priority
7. Generate **Phase 3 Report** → `.claude/reports/phase-3-report.md`:
   ```
   # Phase 3 Report — Epics & Stories
   ## Jira Project: <KEY>
   ## Epic Summary (Table)
   ## Total Stories | Total Points
   ## Sprint Backlog Ready: Yes/No
   ```
8. Run end-of-phase protocol
9. Ask: "All epics and stories are live in Jira. Ready to set up the GitHub repo and tech stack?"

**Do not proceed to Phase 4 until user confirms.**

---

## Phase 4 — GitHub Repo + Tech Stack

**Goal:** Create the GitHub repository, select the tech stack, and wire up CI/CD before any design or code begins.

Steps:
1. **Create GitHub repository:**
   ```bash
   mkdir <project-name> && cd <project-name> && git init
   gh repo create <project-name> --public --source=. --remote=origin
   ```
2. **Copy project scaffold:**
   - `CLAUDE.md` from `~/.claude/templates/project-CLAUDE.md`
   - `.claude/` folder structure created in "Starting a New Project"
3. **Tech stack decision:**
   - Default recommendations:
     - Full-stack web: Next.js 15 + TypeScript + PostgreSQL + Prisma + Tailwind CSS
     - Mobile: React Native + Expo + TypeScript + NativeWind
     - Backend API only: Node.js + Fastify + TypeScript + PostgreSQL + Prisma
     - Backend (large/complex): NestJS + TypeScript + PostgreSQL + Prisma
   - Recommend based on project type with rationale
   - Write decision to `.claude/tech-stack.md`
4. **Scaffold CI/CD pipeline** at `.github/workflows/deploy.yml`:
   ```yaml
   # Trigger: push to main
   # Jobs: lint → test → build → deploy-staging → (manual approval) → deploy-production
   ```
5. **Create GitHub branch protection** on `main`: require PR + passing CI
6. **Create GitHub environments**: `staging` and `production` with required reviewers
7. Generate **Phase 4 Report** → `.claude/reports/phase-4-report.md`:
   ```
   # Phase 4 Report — GitHub Repo + Tech Stack
   ## GitHub Repo: <URL>
   ## Tech Stack Decision
   ## CI/CD Pipeline: configured / not configured
   ## Environments: staging, production
   ```
8. Run end-of-phase protocol (this is the first push to GitHub)
9. Ask: "Repo is live and CI/CD is wired. Ready to hand off to UI/UX for design?"

**Do not proceed to Phase 5 until user confirms.**

---

## Phase 5 — Figma Design (UI/UX Agent)

**Goal:** Produce confirmed designs for every Jira story before any development begins.

**Agile context:** Design is treated as a sprint. Each screen maps to a Jira story. Designs are the Definition of Ready for development.

Setup required before this phase:
- Start WebSocket server: `~/.bun/bin/bun /usr/local/lib/node_modules/claude-talk-to-figma-mcp/dist/socket.js &`
- Open Figma Desktop → Plugins → Development → Claude Talk to Figma Plugin → Run → Connect
- Confirm green "Connected" status

Steps:
1. Ask: "Do you have an existing Figma file? Share the URL or I'll create one."
2. Use Figma MCP to:
   - **Existing file:** Read frames, map to Jira stories, list gaps
   - **New file:** Create frames named after each epic and key story
3. For each screen/frame:
   - Name it: `EPIC-NNN / US-NNN-XXX: <story title>`
   - Note layout decisions in `.claude/design/decisions.md`
   - Add the Figma frame URL to the corresponding Jira story via `editJiraIssue` (custom field or description)
4. Write full frame inventory (Figma URL, frame names, Jira story mapping) to `.claude/design/figma.md`
5. Walk through each screen with the user in chat — confirm or request changes
6. Update Jira stories: transition design-ready stories to "Ready for Development" status via `transitionJiraIssue`
7. Generate **Phase 5 Report** → `.claude/reports/phase-5-report.md`:
   ```
   # Phase 5 Report — Figma Design
   ## Figma File: <URL>
   ## Screens Designed: N
   ## Stories Linked to Frames: N/N
   ## Stories Ready for Development: N
   ## Design Decisions Summary
   ```
8. Run end-of-phase protocol
9. Ask: "All designs confirmed. Ready to start development sprints?"

**Do not proceed to Phase 6 until user confirms.**

---

## Phase 6 — Development (Agile Sprints)

**Goal:** Implement all epics story by story in time-boxed sprints using feature branches.

**Agile context:** 2-week sprints. Backend and frontend run in parallel where possible. Every story transitions through Jira: To Do → In Progress → In Review → Done.

**⚠️ Before writing any code — always do this first:**
1. Read `.claude/database-schema.md` to understand current tables and columns
2. Check if the feature requires a new table or alters an existing one
3. Write the DB migration BEFORE any controller, model, or API code
4. Confirm migration matches the schema doc — never assume column names

**Sprint structure (repeat for each sprint):**

### Sprint Planning
1. Pull "Ready for Development" stories from Jira
2. Select stories for this sprint (target 20–40 points)
3. Transition selected stories to "In Progress" in Jira via `transitionJiraIssue`
4. Create the sprint branch: `git checkout -b sprint/sprint-N`

### Backend Development
1. Build API endpoints for sprint stories
2. Branch per story: `git checkout -b feature/PROJ-NNN-<slug>`
3. After each endpoint: run type check + linter
4. Open PR referencing Jira key — merge to sprint branch
5. Transition Jira story to "In Review" via `transitionJiraIssue`

### Frontend Development
1. Build UI components using Figma designs as the source of truth
2. Branch per story: `git checkout -b feature/PROJ-NNN-<slug>`
3. After each component: run type check + linter
4. Open PR referencing Jira key — merge to sprint branch
5. Transition Jira story to "In Review" via `transitionJiraIssue`

### Sprint Review
1. Demo completed stories against acceptance criteria
2. Transition accepted stories to "Done" in Jira
3. Merge sprint branch to `main` via PR
4. Generate **Sprint N Report** → `.claude/reports/sprint-N-report.md`:
   ```
   # Sprint N Report
   ## Stories Completed: N | Points Delivered: N
   ## Stories Carried Over: N
   ## Velocity: N points
   ## Blockers This Sprint
   ## Next Sprint Goals
   ```
5. Run end-of-phase protocol (commit + push + rsync to staging)
6. Ask: "Sprint N complete. Start Sprint N+1 or move to testing?"

**Do not proceed to Phase 7 until ALL epics are complete and user confirms.**

---

## Phase 7 — Testing

**Goal:** Verify all functionality, security, and user acceptance before deploying to production.

**Agile context:** Testing stories are Jira issues of type "Test". Failed tests become bug issues in Jira.

Steps:
1. **Unit tests:** Write for all business logic functions
2. **Integration tests:** Write for all API endpoints
3. **E2E smoke tests** for the top 3 critical user flows:
   - Web: Playwright
   - Mobile: Detox or Maestro
4. Run full test suite — fix all failures; open Jira bug for each failure, link to affected story

5. **Security checklist (must pass before deploy):**
   - `npm audit` — fix all critical/high vulnerabilities
   - `git log --all -- '*.env'` — confirm no secrets committed
   - All API endpoints validate and sanitize user input
   - Authentication required on all protected routes
   - OWASP Top 10 checklist reviewed

6. **UAT (User Acceptance Testing):**
   - Demo against each epic's acceptance criteria
   - User confirms each epic is working as expected
   - Log any change requests as Jira bugs and fix before proceeding

7. Transition all tested stories to "Done" in Jira
8. Generate **Phase 7 Report** → `.claude/reports/phase-7-report.md`:
   ```
   # Phase 7 Report — Testing
   ## Test Results: X/Y passing
   ## Test Types: unit / integration / E2E
   ## Security Checklist: PASSED / FAILED (list issues)
   ## Bugs Found: N | Bugs Fixed: N | Open: N
   ## UAT: confirmed by <name>
   ```
9. Run end-of-phase protocol
10. Ask: "All tests pass, security checked, UAT confirmed. Ready to deploy to server?"

**Do not proceed to Phase 8 until all tests pass, security checklist is clean, and user confirms UAT.**

---

## Phase 8 — Deploy to Server

**Goal:** Ship to production via staging first. Zero downtime.

Steps:
1. Read `.claude/deployment/server.md` for host, user, app path, PM2 process name, staging URL, production URL
2. Build the production bundle

3. **Step A — Deploy to staging:**
   ```bash
   rsync -avz --exclude node_modules --exclude .git \
     ./dist user@host:/var/www/<project>-staging/
   ssh user@host "cd /var/www/<project>-staging && \
     npm install --production && pm2 restart <process-name>-staging"
   ```
   - Run health check against staging URL
   - Ask user to verify staging before proceeding

4. **Step B — Promote to production (after staging confirmed):**
   ```bash
   rsync -avz --exclude node_modules --exclude .git \
     ./dist user@host:/var/www/<project>/
   ssh user@host "cd /var/www/<project> && \
     npm install --production && pm2 restart <process-name>"
   ```

5. For mobile: `eas build --platform all` and submit to stores

6. **Monitoring setup:**
   - Install and configure Sentry SDK — confirm errors are being captured
   - Confirm PM2 logs: `pm2 logs <process-name>`
   - Set up uptime monitoring (UptimeRobot or similar) on production URL

7. Update `CLAUDE.md` status to `PRODUCTION` with deploy date
8. Generate **Phase 8 Report** → `.claude/reports/phase-8-report.md`:
   ```
   # Phase 8 Report — Deployment
   ## Staging URL: <URL> — Status: OK / FAIL
   ## Production URL: <URL> — Status: OK / FAIL
   ## Deploy Method: rsync + PM2 / EAS
   ## Monitoring: Sentry + PM2 + UptimeRobot
   ## Deploy Date: <date>
   ```
9. Run end-of-phase protocol
10. Tell the user: "Project is live at [URL]. Moving to server testing."

**Do not proceed to Phase 9 until user confirms production is live.**

---

## Phase 9 — Server Testing

**Goal:** Verify production is stable and performing correctly under real conditions.

**Agile context:** Post-deploy bugs become Jira issues of type "Bug" with priority "Critical". Fix and redeploy before proceeding.

Steps:
1. **Smoke tests on production:**
   - Hit all critical API endpoints via `curl` or Playwright
   - Verify authentication flows work end to end
   - Confirm database reads and writes work
   - Verify file uploads, third-party integrations, and webhooks if applicable

2. **Performance checks:**
   - Check response times on key endpoints (target < 200ms p95)
   - Verify memory and CPU are stable under load: `ssh user@host "pm2 monit"`

3. **Log audit:**
   - `pm2 logs <process-name> --lines 100` — check for errors or warnings
   - Confirm Sentry is capturing errors (trigger a test error if needed)

4. **Security spot-check on production:**
   - Verify HTTPS is enforced (no HTTP access)
   - Check security headers (X-Frame-Options, CSP, HSTS)
   - Confirm sensitive env vars are not exposed in any response

5. For any failures:
   - Create Jira bug with priority Critical
   - Fix and redeploy (mini Phase 8)
   - Re-run smoke tests until all pass

6. Generate **Phase 9 Report** → `.claude/reports/phase-9-report.md`:
   ```
   # Phase 9 Report — Server Testing
   ## Smoke Tests: X/Y passed
   ## Performance: p95 response time <Xms
   ## Logs: clean / N errors found and fixed
   ## Security: HTTPS, headers, env vars — PASSED
   ## Critical Bugs Found: N | Fixed: N
   ## Production Status: STABLE
   ```
7. Run end-of-phase protocol
8. Ask: "Server testing passed. Ready to generate the final project report?"

**Do not proceed to Phase 10 until all server tests pass.**

---

## Phase 10 — Final Report

**Goal:** Generate a complete written record of the project for the client and team.

**Agile context:** Close all Jira issues. Archive the sprint board. Tag the GitHub release.

Steps:
1. Close and transition all remaining Jira stories to "Done"
2. Tag a GitHub release:
   ```bash
   git tag -a v1.0.0 -m "Production release"
   git push origin v1.0.0
   gh release create v1.0.0 --title "v1.0.0 — Initial Release" --notes "First production release"
   ```
3. Generate `PROJECT-REPORT.md` in the project root:
   ```
   # Project Report — <Project Name>

   ## Overview
   One paragraph: what was built, why, for whom.

   ## Timeline
   - Date started / date shipped
   - Total phases: 10 | Total sprints: N

   ## Market Research Summary
   - Target market, key competitors, differentiation

   ## Requirements Summary
   - Problem statement | Target users | Core flows | Out of scope

   ## Epics & Stories (Jira)
   - Table: Epic | Jira Key | Stories | Points | Status
   - Total acceptance criteria | Total edge cases

   ## Design
   - Figma file link | Screens designed | Key decisions

   ## Tech Stack
   - Framework, DB, libraries | Rationale

   ## Development (Agile)
   - Total sprints | Total velocity | Features delivered

   ## Testing
   - Tests written: N | Pass rate: X/Y
   - Types: unit / integration / E2E
   - Security: PASSED | UAT: confirmed by <name>

   ## Deployment
   - Platform | Live URL | GitHub repo | GitHub release tag
   - Monitoring: Sentry + PM2 + uptime monitor

   ## Server Testing
   - Smoke tests: X/Y | Performance: p95 <Xms | Status: STABLE

   ## Lessons Learned
   - What went well | What was challenging | What to do differently

   ## Next Steps (v2 Suggestions)
   ```
4. Push `PROJECT-REPORT.md` and all `.claude/reports/*.md` to GitHub
5. Tell the user: "Project complete. Report at PROJECT-REPORT.md. GitHub release v1.0.0 tagged."

---

## Rules

- **GitHub repo is created in Phase 4** — not before, not after
- **Jira is the single source of truth** for all tasks, bugs, and stories — not just local files
- Every phase ends with: report → git commit → git push → rsync to VPS
- Always read the project's `CLAUDE.md` and `.claude/` folder at the start of every session
- Never implement anything before Phase 3 (Jira stories) is confirmed
- Never deploy without Phase 7 tests, security checklist, and UAT passing
- All work happens on branches — never commit directly to `main`
- Run the test suite after every sprint in Phase 6 — never let failures accumulate
- If the user asks "where are we?" summarize the current phase, last sprint, and Jira backlog status
- All Jira issue transitions happen via MCP — never just mark things done locally

---

## Strict Enforcement Rules (Added After Buy2Go Violations)

These rules were added because the buy2go project skipped Phase 3 (Jira), committed directly to `main`, and had no sprint branches. **Never repeat these mistakes.**

1. **HARD STOP at Phase 3** — If Jira epics and stories do not exist, DO NOT write a single line of code. Not even a scaffold. Create the Jira project first.
2. **NEVER commit to `main`** — All work goes on feature branches (`feature/PROJ-NNN-slug`). PRs only.
3. **If a phase was skipped** — Stop everything, go back, and complete that phase retroactively before continuing. Document what was done and update Jira.
4. **At the start of every session** — Read `CLAUDE.md`, check `.claude/jira.md` for the Jira project key, run `searchJiraIssuesUsingJql` to see current backlog status.
5. **The local epic files (`.claude/epics/*.md`) are NOT a substitute for Jira** — They are local mirrors only. Jira is the single source of truth.
6. **Migration stubs are not migrations** — Before deploying, verify every table has its real columns with `SHOW COLUMNS FROM <table>`. Never deploy with `id + timestamps` only tables.

---

## Lessons Learned (Applied to All Future Projects)

### Dependencies
- **Always use `npx expo install <package>` — never `npm install`** for React Native / Expo projects
  - `npx expo install` picks the SDK-compatible version automatically
  - Run it for every package: reanimated, async-storage, etc.

### Build
- **Run a test EAS build at the end of Phase 6 (Development), not Phase 8 (Deploy)**
  - Catch build errors early: `eas build --profile preview --platform android --non-interactive`
  - Fix all build errors before Phase 7 (Testing)

### Figma MCP
- **Set up the Figma MCP plugin before Phase 5 begins — not during it**
  1. Start WebSocket server: `~/.bun/bin/bun /usr/local/lib/node_modules/claude-talk-to-figma-mcp/dist/socket.js &`
  2. Open Figma Desktop → Plugins → Development → Claude Talk to Figma Plugin → Run → Connect
  3. Confirm green "Connected" status

### Jira MCP
- **Always check `getVisibleJiraProjects` first** — don't create a duplicate project
- Use `searchJiraIssuesUsingJql` to query current sprint status before planning the next
- Always store the Jira project key in `.claude/jira.md` at the start of Phase 3

### Database
- Read `.claude/database-schema.md` before any code — never assume column names
- Write migrations before controllers — always
- **Verify every table has real columns before deploying** — run `SHOW COLUMNS FROM <table>` on the VPS. Stub migrations (`id + timestamps` only) will silently fail on the first INSERT.
- **After any fresh DB deploy** — run `php artisan migrate:status` and manually spot-check 5 key tables

### VPS / Server
- **Always fill in `.claude/deployment/server.md`** with host, user, app path, PM2 name, SSH key location
- **Never assume rsync = deployed** — SSH in and verify the running process, PHP/Node version, and DB connection after every deploy
- **Store SSH credentials securely** — the server.md template has placeholders; fill them or store in a password manager and reference them
- **APP_DEBUG must be false in production** — check `.env` on the VPS after every deploy

### Flutter / Android Build
- **Java 17 is required for Gradle 7.5** — Android Studio 2025+ ships Java 21 which breaks Gradle 7.5. Download Temurin 17 from Adoptium and set `JAVA_HOME` explicitly.
  - Download: `https://github.com/adoptium/temurin17-binaries/releases`
  - Build command: `JAVA_HOME="/path/to/jdk17" flutter run -d emulator-5554 -t lib/main_new.dart`
- **Always check which `main.dart` to use** — old Flutter apps often have `main.dart` (old design) and `main_new.dart` (new design). Run with `-t lib/main_new.dart` for the new design.
- **Kotlin version must match plugins** — if `location` or other plugins were compiled with Kotlin 1.9, set `ext.kotlin_version = '1.9.24'` in `android/build.gradle`.
- **AGP 8+ requires `namespace`** in `app/build.gradle`: add `namespace 'com.your.package'` to the `android {}` block.
- **Storage permissions on first deploy**: always run `php artisan storage:link` and `chmod -R 775 storage/` after rsync.

### Staff / User Role Mismatch (Buy2Go Lesson)
- **Controller-written roles must match query-expected roles** — e.g., `staffController.registerStaff` writes `user_role = 'Brand manager'` but `getBrandManagers` queries `user_role = 'BRANDS'`. Always grep the codebase for both sides before shipping.
- **users.name, users.password must be nullable** if staff users are created without passwords (OTP-based login). Add this to migrations from day one.
