---
name: deploy
description: Full Phase 9 deployment to Hostinger VPS — builds, syncs, restarts PM2, and runs health check.
---

1. Read .claude/deployment/server.md — extract HOST, USER, APP_PATH, PM2_NAME, PRODUCTION_URL
2. Run the full test suite — STOP if any test fails. Never deploy broken code.
3. Confirm with user: "About to deploy to {PRODUCTION_URL}. All tests pass. Proceed?"
4. Build production bundle: `npm run build`
5. Sync to server:
   ```bash
   rsync -avz --exclude node_modules --exclude .git ./dist {USER}@{HOST}:{APP_PATH}
   ```
6. Install & restart:
   ```bash
   ssh {USER}@{HOST} "cd {APP_PATH} && npm install --production && pm2 restart {PM2_NAME}"
   ```
7. Health check: `curl -f https://{PRODUCTION_URL}/health`
8a. If health check PASSES:
    - Update project CLAUDE.md: set Deployment Status = PRODUCTION, add date
    - Commit: `git add CLAUDE.md && git commit -m "chore: deployed to production [date]"`
    - Tell user: "Live at {PRODUCTION_URL}"
8b. If health check FAILS:
    - Roll back: `ssh {USER}@{HOST} "pm2 restart {PM2_NAME} --update-env"`
    - Show the error log
    - Do NOT mark as deployed
