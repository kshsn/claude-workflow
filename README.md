# Claude Dev Workflow

My personal Claude Code workflow for building products from idea to production.

## Pipeline

```
[1] Requirements → [2] Epics & Stories → [3] Figma Design → [4] Tech Stack → [5] Build → [6] Test → [7] Deploy
```

Each phase gates the next. Claude waits for confirmation before advancing.

## Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Global workflow rules — Claude reads this at the start of every session |
| `templates/project-CLAUDE.md` | Template for per-project CLAUDE.md (phase tracker) |
| `templates/requirements.md` | Phase 1 — structured requirements template |
| `templates/epic.md` | Phase 2 — epic with user stories, AC, edge cases |
| `templates/server.md` | Phase 7 — Hostinger VPS deployment config |
| `pipeline-design.md` | Original plan document for this workflow |

## Setup

1. Clone this repo
2. Copy `CLAUDE.md` to `~/.claude/CLAUDE.md`
3. Copy `templates/` to `~/.claude/templates/`
4. Claude will automatically follow the pipeline for every new project

## Key Rules

- **Always create a GitHub repo at the very start of a new project**
- Never implement before Phase 4 is confirmed
- Never deploy without Phase 6 tests passing
- Commit and push to GitHub after each completed phase
- For mobile apps: use Expo EAS Build for APK (Android) and IPA (iOS)
