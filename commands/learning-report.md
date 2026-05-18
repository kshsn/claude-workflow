---
name: learning-report
description: Generate a full report of all lessons learned — grouped by category, with frequency analysis and action items.
argument-hint: [YYYY-MM for monthly filter, or leave blank for all-time]
---

Steps:
1. Run the report generator:
   ```bash
   python "C:/Users/Khaled/.claude/scripts/generate-report.py" $ARGUMENTS
   ```
2. Read the generated report from `~/.claude/reports/learning-report-*.md`
3. Display the full report to the user
4. Provide a brief interpretation:
   - Which category has the most repeated mistakes?
   - Are there patterns that should become permanent hooks instead of just lessons?
   - Which lessons seem "mastered" (not repeated in 30+ days)?
5. Recommend specific actions:
   - "Add X to lessons-learned.md as a permanent rule"
   - "Consider a hook for Y since it happened N times"
   - "These Z lessons can be removed — Claude does them correctly now"
6. Ask: "Should I push this report to GitHub and update lessons-learned.md with the high-frequency rules?"
7. If yes:
   - Update `~/.claude/docs/lessons-learned.md` with any new permanent rules
   - Copy report to the claude-workflow repo and push
   - Commit: `git add docs/lessons-learned.md && git commit -m "docs: update lessons from learning report"`
