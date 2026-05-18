---
name: new-device
description: Orientation guide for a new device. Shows how Claude functions and learns, then checks VPS connection and walks through setup if needed.
argument-hint: (no arguments needed)
---

Display exactly this guide to the user, then check VPS connection at the end.

---

# New Device Setup & Claude Orientation

## 1. Install the workflow (if not done yet)

```bash
git clone https://github.com/kshsn/claude-workflow
cd claude-workflow

# Windows:
.\install.ps1

# Mac / Linux:
chmod +x install.sh && ./install.sh
```

The installer copies all files to `~/.claude/` and asks if you want to connect to the VPS lesson database.

---

## 2. How Claude functions

### The pipeline — every project follows this sequence:
```
[1] Requirements → [2] Planning → [3] Plan Report → [4] Epics & Stories →
[5] Figma Design → [6] Tech Stack → [7] Build → [8] Test → [9] Deploy → [10] Report
```
Each phase needs your confirmation before moving forward. Use `/phase-start` to begin any phase.

### Commands:
| Command | What it does |
|---|---|
| `/new-device` | This guide |
| `/phase-start` | Begin a project phase |
| `/epic-start` | Break phase into epics and stories |
| `/where-are-we` | Show current phase status |
| `/lesson <text>` | Log a lesson right now |
| `/recall` | Pull all lessons from VPS database |
| `/recall git` | Filter lessons by category |
| `/learning-report` | Full lesson analysis with trends |
| `/deploy` | Deploy the current project |
| `/pr-describe` | Write a pull request description |
| `/test-triage` | Analyze failing tests |

### Specialist agents:
| Agent | When Claude uses it |
|---|---|
| `requirements-agent` | Phase 1 — capturing what to build |
| `epic-writer-agent` | Phase 4 — epics and user stories |
| `test-runner-agent` | Phase 8 — running and triaging tests |
| `deploy-agent` | Phase 9 — deploying to server |
| `security-reviewer-agent` | Before every single commit |

### Git rules:
- One file per commit — never `git add .`
- Never force-push to main or master
- Create the GitHub repo before writing any code
- Security review before every commit

---

## 3. How Claude learns

### The learning pipeline:
```
You correct Claude
  → detect-correction.py fires instantly
  → Draft lesson auto-saved to VPS (guaranteed capture)
  → Claude calls /lesson with precise text
  → Refined lesson saved locally + synced to VPS

Next session starts
  → session-start.py fetches last 5 lessons from VPS
  → Injects them into Claude's context
  → Claude starts already knowing recent mistakes
```

### Three layers — nothing is ever missed:
1. **Auto-capture** — when you type a correction ("no", "that's wrong", "you missed"), the hook logs a draft to VPS *before* Claude even responds
2. **Refined capture** — Claude calls `/lesson` after fixing the issue, adding the root cause
3. **Session memory** — every session start loads the last 5 lessons from VPS automatically

### Lesson categories:
`dependencies` | `build` | `hooks` | `testing` | `deployment` | `git` | `security` | `design` | `workflow` | `general`

### Where lessons live:
- **Local**: `~/.claude/logs/lessons.jsonl` — written first, always works offline
- **VPS**: PostgreSQL at `89.116.236.22:4000` — synced after every lesson, accessible from any device

---

## 4. Files on this device

After install, `~/.claude/` contains:
```
CLAUDE.md             ← core rules and pipeline
settings.json         ← all hooks wired up
lessons-api.json      ← VPS credentials (never commit this file)
hooks/                ← auto-run on tool use and session events
commands/             ← all /slash commands including this one
agents/               ← specialist subagents
rules/                ← path-scoped rules (auto-loaded by file type)
docs/                 ← phase details, security guide, lessons learned
scripts/              ← lesson logging, VPS sync, recall
logs/                 ← local lessons.jsonl + session log
```

---

## 5. VPS connection check

Now run this to verify lessons are syncing:

```bash
python ~/.claude/scripts/recall-lessons.py
```

**If output shows lessons from VPS** → this device is fully connected. You are ready.

**If output says "VPS unreachable"** → run:
```bash
python ~/.claude/scripts/setup-vps-config.py
```
Enter the API URL (`http://89.116.236.22:4000`) and the API key from `lessons-api.json` on your primary device. Then run the recall script again to confirm.
