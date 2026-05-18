# Claude Global Workflow

Production-ready Claude Code global configuration — hooks, slash commands, subagents, path-scoped rules, security, and templates built to expert standards.

## What's Inside

```
claude-workflow/
├── CLAUDE.md                    ← Global rules (copied to ~/.claude/CLAUDE.md)
├── settings.template.json       ← Hooks config (installer generates settings.json)
├── hooks/                       ← Python hook scripts (auto-run by Claude Code)
│   ├── block-secrets.py         ← Blocks API keys/tokens from being written to files
│   ├── block-dangerous-commands.py ← Blocks rm -rf /, force push to main, DROP DATABASE
│   ├── format-on-write.py       ← Auto-formats TS/JS/Python after every file write
│   ├── notify-stop.py           ← Logs session end
│   └── session-start.py         ← Logs session start, reminds Claude to read CLAUDE.md
├── commands/                    ← Slash commands (type / in Claude Code to use)
│   ├── phase-start.md           ← /phase-start  — begin any project phase
│   ├── epic-start.md            ← /epic-start   — create and build an epic
│   ├── where-are-we.md          ← /where-are-we — full project status summary
│   ├── pr-describe.md           ← /pr-describe  — auto-generate PR description
│   ├── changelog.md             ← /changelog    — generate changelog from git log
│   ├── test-triage.md           ← /test-triage  — run tests, explain failures, fix
│   └── deploy.md                ← /deploy       — full VPS deploy with health check
├── agents/                      ← Specialist subagents (right model per job)
│   ├── requirements-agent.md    ← Phase 1: structured requirements (Haiku)
│   ├── epic-writer-agent.md     ← Phase 4: BDD epics and stories (Sonnet)
│   ├── test-runner-agent.md     ← Phase 8: write and run tests (Sonnet)
│   ├── deploy-agent.md          ← Phase 9: safe deployment (Sonnet)
│   └── security-reviewer-agent.md ← Pre-commit OWASP scan (Sonnet, proactive)
├── rules/                       ← Path-scoped rules (lazy-loaded per file type)
│   ├── api-rules.md             ← Loads for *.route.ts, controllers/**, api/**
│   ├── frontend-rules.md        ← Loads for *.tsx, *.jsx, components/**
│   ├── testing-rules.md         ← Loads for *.test.ts, *.spec.ts, tests/**
│   └── git-rules.md             ← Loads globally (all files)
├── docs/                        ← Detailed phase docs and reference
│   ├── phases-1-3.md            ← Requirements → Planning → Plan Report
│   ├── phases-4-6.md            ← Epics & Stories → Figma → Tech Stack
│   ├── phases-7-10.md           ← Build → Test → Deploy → Report
│   ├── lessons-learned.md       ← Rules from real past project mistakes
│   └── security.md              ← OWASP Top 10 checklist + secrets management
└── templates/                   ← Project starter templates
    ├── project-CLAUDE.md        ← Per-project CLAUDE.md with phase checklist
    ├── requirements.md          ← Structured requirements document
    ├── epic.md                  ← Epic + user story + acceptance criteria
    └── server.md                ← VPS deployment config
```

---

## Install on a New Device

### Windows
```powershell
git clone https://github.com/kshsn/claude-workflow.git
cd claude-workflow
.\install.ps1
```

### Mac / Linux
```bash
git clone https://github.com/kshsn/claude-workflow.git
cd claude-workflow
chmod +x install.sh && ./install.sh
```

The installer copies everything to `~/.claude/` and generates `settings.json` with correct absolute paths for your machine.

---

## Update an Existing Install
```bash
cd claude-workflow && git pull
.\install.ps1   # Windows
./install.sh    # Mac / Linux
```

---

## 10-Phase Development Pipeline

```
[1] Requirements → [2] Planning → [3] Plan Report → [4] Epics & Stories →
[5] Figma Design → [6] Tech Stack → [7] Build → [8] Test → [9] Deploy → [10] Report
```

Start any project: tell Claude **"start a new project"**
Check status anytime: **/where-are-we**
