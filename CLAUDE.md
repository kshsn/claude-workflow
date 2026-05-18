# Claude Global Workflow

## Pipeline
```
[1] Requirements → [2] Planning → [3] Plan Report → [4] Epics & Stories →
[5] Figma Design → [6] Tech Stack → [7] Build → [8] Test → [9] Deploy → [10] Report
```
Each phase requires explicit user confirmation. Never skip a phase.
Use `/phase-start` to begin any phase. Use `/where-are-we` to check status.

---

## Starting a New Project
When user says "start a new project" or describes an idea:
1. Ask for the project name
2. Create GitHub repo immediately (before any code):
   ```bash
   mkdir <name> && cd <name> && git init
   gh repo create <name> --public --source=. --remote=origin
   ```
3. Scaffold from `~/.claude/templates/project-CLAUDE.md`
4. Invoke `requirements-agent` for Phase 1

Phase details: `~/.claude/docs/phases-1-3.md` | `phases-4-6.md` | `phases-7-10.md`

---

## Specialist Agents (use these — don't do everything yourself)
| Agent | Phase | Model |
|-------|-------|-------|
| `requirements-agent` | Phase 1 | Haiku |
| `epic-writer-agent` | Phase 4 | Sonnet |
| `test-runner-agent` | Phase 8 | Sonnet |
| `deploy-agent` | Phase 9 | Sonnet |
| `security-reviewer-agent` | Before every commit | Sonnet |

---

## Slash Commands Available
`/phase-start` `/epic-start` `/where-are-we` `/pr-describe`
`/changelog` `/test-triage` `/deploy`

---

## Default Tech Stacks
| Project Type | Stack |
|---|---|
| Full-stack web | Next.js 14 + TypeScript + PostgreSQL + Prisma + Tailwind |
| Mobile | React Native + Expo + TypeScript + NativeWind |
| Backend API | Node.js + Fastify + TypeScript + PostgreSQL + Prisma |
| Backend (complex) | NestJS + TypeScript + PostgreSQL + Prisma |

---

## Core Rules
- Create GitHub repo before writing any code
- Read project `CLAUDE.md` + `.claude/` at the start of every session
- Never implement before Phase 4 is confirmed
- Never deploy without Phase 8 tests passing
- Run `security-reviewer-agent` before every commit
- Commit one file at a time — never `git add .`

## Git: One Commit Per File
```bash
git add src/login.ts && git commit -m "feat: add login handler"
git add src/login.test.ts && git commit -m "test: add login unit tests"
```

## Context Management
- Run `/compact` at ~50% context usage
- Keep each task completable within 50% context window
- Use agents with `context: fork` for isolated subtasks to protect main context

## Model Selection
- Haiku → simple reads, searches, formatting, requirements capture
- Sonnet → standard coding, testing, code review (default)
- Opus → architecture decisions, complex debugging, design trade-offs

---

## References
- Security: `~/.claude/docs/security.md`
- Lessons learned: `~/.claude/docs/lessons-learned.md`
- Path rules: `~/.claude/rules/` (auto-loaded per file type)
