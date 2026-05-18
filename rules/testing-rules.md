---
description: Rules for all test files — unit, integration, and E2E
paths: ["**/*.test.ts", "**/*.spec.ts", "**/*.test.tsx", "**/*.spec.tsx", "tests/**", "__tests__/**", "e2e/**"]
---

# Testing Rules (BDD Methodology)

## Structure
- Every test: Arrange → Act → Assert (one assertion per test where possible)
- Test names must describe behavior: "returns 401 when token is expired" not "auth test"
- Group related tests in `describe` blocks named after the unit under test
- Use `beforeEach` for setup, `afterEach` for cleanup — never share mutable state between tests

## What to Test
- Test behavior and outcomes — not implementation details or private methods
- Test the public interface only
- Always test edge cases: null/undefined input, empty arrays, max/min values, concurrent calls

## What NOT to Do
- Never mock the database in integration tests — use a real test database with test data
- Never test framework code (Next.js routing, Expo navigation) — only test your logic
- Never leave `.only` or `.skip` in committed test files — they hide failures
- Never use `setTimeout` for async waiting — use `waitFor`, fake timers, or proper async/await

## Commit Rule
Each test file gets its own commit:
```bash
git add src/auth/login.test.ts && git commit -m "test: add login handler unit tests"
```

## React Native / Expo
- Use `npx expo install` for all test packages
- Run `eas build --profile preview --platform android` at end of Phase 7 to catch build errors early
