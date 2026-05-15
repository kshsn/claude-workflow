# Plan: End-to-End Product Development Workflow

## Context

The user wants a repeatable, structured pipeline where they describe an idea and Claude handles everything from product specs → design → build → deploy. Projects will be full-stack or mobile apps. Progress is tracked in markdown files (CLAUDE.md + `.claude/` folder). Figma is connected via MCP using a personal API token. Deployment targets a Hostinger VPS via SSH.

---

## Overview of the 7-Phase Pipeline

```
[1] Requirements → [2] Epics & Stories → [3] Figma Design → [4] Tech Decision → [5] Build → [6] Test → [7] Deploy
```

Each phase gates the next. Claude waits for user confirmation before advancing.

---

## What Gets Built

### 1. Global Workflow Definition (`~/.claude/CLAUDE.md`)
Teaches Claude the pipeline rules so every new project follows the same process automatically.

### 2. Figma MCP Configuration (`~/.claude/settings.json`)
Adds the Figma MCP server so Claude can create and inspect Figma designs.

### 3. Per-Project Scaffold
Every new project gets initialized with this structure:

```
project-root/
├── CLAUDE.md                        ← project context + current phase tracker
└── .claude/
    ├── requirements.md              ← raw idea + structured requirements
    ├── epics/
    │   └── epic-NNN-<name>.md       ← one file per epic
    ├── design/
    │   ├── figma.md                 ← Figma file links + frame inventory
    │   └── decisions.md             ← confirmed design decisions
    ├── tech-stack.md                ← language/framework decision + rationale
    └── deployment/
        └── server.md               ← Hostinger VPS config (host, user, paths)
```

### 4. `init-project` slash command behavior (via global CLAUDE.md)
When user says "start a new project", Claude:
- Creates the folder structure above
- Asks for the project name and rough idea
- Moves to Phase 1

---

## Phase Details

### Phase 1 — Requirements Capture
**Trigger:** User describes an idea (can be rough)  
**Claude does:**
- Asks clarifying questions (target users, key actions, constraints, non-goals)
- Writes structured requirements to `.claude/requirements.md`
- Format: Problem statement, Goals, Non-goals, Key user types, Core flows (numbered)
**Gate:** User confirms requirements are complete

### Phase 2 — Epics, User Stories, AC & Edge Cases
**Trigger:** Requirements confirmed  
**Claude does:**
- Groups features into 2–6 epics
- Each epic file (`.claude/epics/epic-NNN-<name>.md`) contains:
  ```
  # Epic NNN: <Name>
  **Goal:** one sentence
  
  ## Stories
  ### US-001: As a <user>, I want to <action> so that <value>
  **Acceptance Criteria:**
  - [ ] Given X, when Y, then Z
  - [ ] ...
  **Edge Cases:**
  - What if the user has no data yet?
  - What if the network drops mid-action?
  - What if permissions are denied?
  ```
- Writes a summary index to `requirements.md`
**Gate:** User approves epics or requests changes

### Phase 3 — Figma Design
**Trigger:** Epics approved  
**Claude does:**
- Uses Figma MCP to read an existing Figma file if user provides a URL, OR
- Creates a new Figma file via MCP and scaffolds frames per epic
- Links frames to stories in `.claude/design/figma.md`
- Presents frame-by-frame design review in chat
**Gate:** User confirms each screen / marks design done in `decisions.md`

**Figma MCP setup required:**
- Add Figma MCP to `~/.claude/settings.json` with user's personal access token
- MCP server: `@figma/mcp-server` (official Figma MCP)

### Phase 4 — Tech Stack Decision
**Trigger:** Design confirmed  
**Claude does:**
- Recommends stack based on project type (full-stack vs mobile):
  - Full-stack default: Next.js + TypeScript + PostgreSQL + Prisma
  - Mobile default: React Native + Expo + TypeScript
  - Backend: Node.js (Express or Fastify) or NestJS for larger apps
- Documents choice + rationale in `.claude/tech-stack.md`
- Lists dependencies, folder structure, tooling
**Gate:** User selects/overrides stack

### Phase 5 — Build
**Trigger:** Stack decided  
**Claude does:**
- Scaffolds the project with chosen framework
- Implements epics story by story (US-001, US-002, ...)
- Marks each story `[x]` in the epic file when done
- Runs type checks + linter after each epic
- Updates `CLAUDE.md` current phase

### Phase 6 — Testing
**Trigger:** Build complete  
**Claude does:**
- Unit tests for business logic
- Integration tests for API endpoints
- E2E smoke test for critical user flows (Playwright for web, Detox for mobile)
- Runs full test suite and reports results
**Gate:** All tests pass before deploy

### Phase 7 — Deploy to Hostinger VPS
**Trigger:** Tests pass  
**Claude does:**
- Reads `.claude/deployment/server.md` for VPS details (host, user, app path)
- For full-stack: builds production bundle, rsyncs to VPS, restarts PM2 process
- For mobile: runs `eas build` (Expo) or triggers store upload
- Verifies deployment with a health-check request
- Marks project as `PRODUCTION` in `CLAUDE.md`

**SSH deployment pattern:**
```bash
rsync -avz --exclude node_modules ./dist user@host:/var/www/project
ssh user@host "cd /var/www/project && pm2 restart app"
```

---

## Files to Create

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | Global workflow rules for Claude |
| `~/.claude/settings.json` | Figma MCP config |
| `~/.claude/templates/project-CLAUDE.md` | Template for per-project CLAUDE.md |
| `~/.claude/templates/epic.md` | Epic file template |
| `~/.claude/templates/requirements.md` | Requirements template |
| `~/.claude/templates/server.md` | Deployment config template |

---

## Verification

1. Create a test project folder, run the init flow, confirm folder structure is created
2. Enter a sample idea → verify epic files are generated with correct AC format
3. Provide a Figma token → verify MCP connects and Claude can read/create frames
4. Confirm design → verify `decisions.md` is updated
5. Pick a stack → verify scaffold is generated
6. Run tests → verify suite runs
7. Trigger deploy → verify SSH commands run against Hostinger VPS and app responds

---

## Open Question

Need the user's Figma personal access token to wire up MCP. Will ask during execution.
