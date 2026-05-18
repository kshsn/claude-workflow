---
name: new-device
description: First-time setup and orientation for a new device. Explains how Claude functions, how it learns, and connects this device to the VPS lesson database.
argument-hint: (no arguments needed)
---

Run the following steps in order:

## Step 1 — Check VPS connection

```bash
python "~/.claude/scripts/recall-lessons.py" --limit 1
```

If the output says "VPS unreachable", run setup:

```bash
python "~/.claude/scripts/setup-vps-config.py"
```

When prompted:
- API URL: `http://89.116.236.22:4000`
- API key: (copy from `~/.claude/lessons-api.json` on your primary device)

After setup, confirm with:

```bash
python "~/.claude/scripts/recall-lessons.py"
```

---

## Step 2 — Display this orientation guide

Tell the user:

---

# How I Function

## My Pipeline
Every project I work on follows this 10-phase pipeline:
```
[1] Requirements → [2] Planning → [3] Plan Report → [4] Epics & Stories →
[5] Figma Design → [6] Tech Stack → [7] Build → [8] Test → [9] Deploy → [10] Report
```
Each phase needs your explicit confirmation before I move to the next one.

## Commands You Can Use
| Command | What it does |
|---|---|
| `/phase-start` | Begin a new project phase |
| `/epic-start` | Break a phase into epics and user stories |
| `/where-are-we` | Show current phase and what's done |
| `/recall` | Pull all lessons I've learned from the database |
| `/lesson <text>` | Log a new lesson right now |
| `/learning-report` | Full analysis of lessons by category |
| `/new-device` | This guide — run on any new device |
| `/deploy` | Deploy the current project |
| `/pr-describe` | Write a PR description |
| `/test-triage` | Analyze failing tests |

## Specialist Agents I Use
| Agent | When |
|---|---|
| `requirements-agent` | Phase 1 — capture requirements |
| `epic-writer-agent` | Phase 4 — write epics and stories |
| `test-runner-agent` | Phase 8 — run and triage tests |
| `deploy-agent` | Phase 9 — deploy to server |
| `security-reviewer-agent` | Before every commit |

## My Git Rules
- One commit per file — never `git add .`
- Always create a GitHub repo before writing code
- Never force-push to main/master
- Never skip the security review before committing

---

# How I Learn

## The Learning Pipeline
```
You correct me → hook auto-logs a draft to the database immediately
Claude calls /lesson → refined entry saved locally + synced to VPS
Session starts next time → last 5 lessons loaded into my context
/recall → you can review everything from any device
```

## Three-Layer Capture (nothing is missed)
1. **Auto-capture** — when you type a correction ("no don't", "that's wrong", etc.)
   the `detect-correction.py` hook fires instantly and logs a draft entry to the
   VPS database before I even respond.

2. **Refined capture** — I call `/lesson` after fixing the issue, writing a precise
   entry with the root cause. This syncs to VPS automatically.

3. **Session memory** — every time a session starts, `session-start.py` fetches
   the last 5 lessons from the VPS and injects them into my context so I start
   already knowing what I got wrong recently.

## Where Lessons Live
- **Local**: `~/.claude/logs/lessons.jsonl` — always written first
- **VPS**: PostgreSQL at `89.116.236.22:4000` — synced after every lesson
- **Fallback**: if VPS is unreachable, local JSONL keeps the record

## Lesson Categories
`dependencies` | `build` | `hooks` | `testing` | `deployment` | `git` | `security` | `design` | `workflow` | `general`

## To Review What I've Learned
```
/recall              → all lessons
/recall git          → only git lessons
/recall hooks --limit 5  → last 5 hook lessons
/learning-report     → full analysis with trends
```

---

# Files on This Device

After install, your `~/.claude/` folder has:
```
~/.claude/
  CLAUDE.md             ← my core rules and pipeline
  settings.json         ← hooks wired to all scripts
  lessons-api.json      ← your VPS credentials (never commit this)
  hooks/                ← auto-run on every tool use / session
  commands/             ← all /slash commands
  agents/               ← specialist subagents
  rules/                ← path-scoped rules (auto-loaded per file type)
  docs/                 ← phase details, security guide, lessons learned
  scripts/              ← lesson logging, VPS sync, recall
  logs/                 ← local lessons.jsonl + session log
```

---

Step 3 — Confirm setup is complete by running:

```bash
python "~/.claude/scripts/recall-lessons.py"
```

If lessons appear from VPS, this device is fully connected. You're ready.
