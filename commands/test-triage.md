---
name: test-triage
description: Run the test suite, identify all failures, explain root causes, and suggest specific fixes.
---

1. Detect the test runner from package.json scripts:
   - Jest: `npx jest --json 2>/dev/null | tail -1`
   - Vitest: `npx vitest run --reporter=json`
   - Playwright: `npx playwright test --reporter=json`
   - Pytest: `python -m pytest --tb=short`
2. Run the test suite and capture output
3. For each failing test:
   - Show: test name, error message, file location
   - Read the relevant source file
   - Identify root cause: logic error / wrong assertion / missing mock / env issue / race condition
   - Write a specific fix (code snippet)
4. Group failures by root cause to spot systemic issues
5. Output a triage report:

   ```
   ## Test Triage Report
   Total: X passing, Y failing

   ### Failures by Root Cause
   **[Cause]** (N tests affected)
   - test/auth.spec.ts:42 — [error summary]
   - Fix: [specific code change]
   ```

6. Ask: "Should I apply these fixes now?"
