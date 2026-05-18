---
name: pr-describe
description: Auto-generate a pull request title and full description from git history and diff.
---

1. Run: `git log main..HEAD --oneline` — list all commits on this branch
2. Run: `git diff main..HEAD --stat` — see changed files summary
3. Run: `git diff main..HEAD` — read the full diff
4. Generate a complete PR description:

   **Title** (under 70 chars, imperative mood — e.g. "Add JWT authentication to API endpoints")

   **Summary**
   - What changed and why (3 bullet points max)

   **Test plan**
   - [ ] Step to verify feature works
   - [ ] Edge case to check
   - [ ] Regression check

   **Breaking changes** (list any, or "None")

5. Output the full markdown — ready to paste into GitHub
6. Ask: "Should I create the PR now with `gh pr create`?"
7. If yes: run `gh pr create --title "..." --body "..."` with the generated content
