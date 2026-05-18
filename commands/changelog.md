---
name: changelog
description: Generate a changelog from git log since the last tag or a given ref.
argument-hint: [since-tag-or-date]
---

1. Determine the starting point:
   - If $ARGUMENTS given: `git log {arg}..HEAD --oneline`
   - Otherwise: `git log $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD --oneline`
2. Group commits by prefix type:
   - `feat:` → Features
   - `fix:` → Bug Fixes
   - `refactor:` / `perf:` → Improvements
   - `docs:` / `test:` / `chore:` → Docs & Chores
3. Format as markdown:

   ```
   ## [Unreleased] — YYYY-MM-DD

   ### Features
   - ...

   ### Bug Fixes
   - ...

   ### Improvements
   - ...

   ### Docs & Chores
   - ...
   ```

4. Prepend to CHANGELOG.md (create if it doesn't exist)
5. Commit: `git add CHANGELOG.md && git commit -m "docs: update changelog"`
6. Show the output to the user
