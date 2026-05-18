---
description: Git commit and branch rules — loaded globally for all files
paths: ["**/*"]
---

# Git Rules

## Commit Standard: One Commit Per File
Create a separate commit for each file changed. Never bundle multiple files into one commit.

```bash
# Correct — one file, one commit:
git add src/auth/login.ts && git commit -m "feat: add JWT login handler"
git add src/auth/login.test.ts && git commit -m "test: add login handler unit tests"
git add CLAUDE.md && git commit -m "docs: mark Phase 1 complete"

# Wrong — never do this:
git add . && git commit -m "add auth feature"
```

## Commit Message Format
```
type(scope): short description under 72 chars

Types: feat | fix | docs | test | refactor | chore | style | phase | epic
```

## Branch Strategy
- Feature branches: `feat/epic-001-auth`, `fix/login-redirect`, `docs/update-readme`
- Never commit directly to `main` or `master` — always use a PR
- Never force-push to `main` or `master`

## Safety Checklist Before Every Commit
- [ ] Run: `git diff --staged` to review exactly what you're committing
- [ ] No `.env` files in the staged list
- [ ] No API keys, tokens, or passwords in the diff
- [ ] Type check passes: `tsc --noEmit`
- [ ] Linter passes: `eslint .` or `npx biome check .`

## What Never to Commit
- `.env` (use `.env.example` for documentation)
- `node_modules/`, `dist/`, `.next/`, `build/`, `.expo/`
- API keys, tokens, private keys, database dumps
- Editor files: `.DS_Store`, `Thumbs.db`, `.vscode/settings.json`
