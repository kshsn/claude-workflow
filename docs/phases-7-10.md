# Phases 7–10: Build, Test, Deploy & Report

---

## Phase 7 — Build
**Goal:** Implement all epics story by story.

Steps:
1. Scaffold the project with the chosen framework
2. Work through epics in order (epic-001 first)
3. Within each epic, implement stories in order (US-001, US-002, ...)
4. After each story:
   - Mark it `[x]` in the epic file
   - Run type check and linter
5. After each epic:
   - Update project `CLAUDE.md` with current phase and last completed epic
   - Ask: "Epic [N] is done. Ready to continue to the next epic?"

> **Gate:** Do not proceed to Phase 8 until all epics are complete and user confirms.

---

## Phase 8 — Testing
**Goal:** Verify all functionality before deploying.

Steps:
1. Write unit tests for all business logic functions
2. Write integration tests for all API endpoints
3. Write E2E smoke tests for the top 3 critical user flows:
   - Web: Playwright
   - Mobile: Detox or Maestro
4. Run the full test suite — fix all failures before continuing
5. Report results: X/Y tests passing
6. Ask: "All tests pass. Ready to deploy?"

> **Gate:** Do not proceed to Phase 9 until all tests pass and user confirms.

---

## Phase 9 — Deploy to Hostinger VPS
**Goal:** Ship to production.

Steps:
1. Read `.claude/deployment/server.md` for host, user, app path, PM2 process name
2. Build the production bundle
3. For full-stack / web:
   ```bash
   rsync -avz --exclude node_modules --exclude .git ./dist user@host:/var/www/<project>
   ssh user@host "cd /var/www/<project> && npm install --production && pm2 restart <name>"
   ```
4. For mobile: run `eas build --platform all` and submit to stores
5. Verify with a health-check HTTP request to the production URL
6. Update project `CLAUDE.md` status to `PRODUCTION` with deploy date
7. Tell the user: "Project is live at [URL]."

---

## Phase 10 — Project Report
**Goal:** Generate a full written record of the completed project.

Sections for `PROJECT-REPORT.md`:
- Overview, Timeline, Requirements Summary
- Epics & Stories (table: Epic | Stories | Status)
- Design (Figma link, screen count, key decisions)
- Tech Stack (framework, libraries, reasoning)
- Testing (total tests, pass rate, test types)
- Deployment (platform, build tool, live URL, GitHub link)
- Lessons Learned (what went well / challenges / what to change)
- Next Steps (v2 suggestions)

After generating: push `PROJECT-REPORT.md` to GitHub and notify the user.
