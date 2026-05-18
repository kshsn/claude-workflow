#!/usr/bin/env python3
"""
generate-report.py — reads lessons.jsonl and produces a markdown learning report.

Usage:
  python generate-report.py                  # all-time report
  python generate-report.py 2026-05          # filter to month
  python generate-report.py --stdout         # print only, don't save
"""
import json
import os
import sys
from datetime import datetime
from collections import defaultdict, Counter

LESSONS_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'lessons.jsonl')
REPORTS_DIR  = os.path.join(os.path.expanduser('~'), '.claude', 'reports')

def load_lessons(period=None):
    if not os.path.exists(LESSONS_FILE):
        return []
    lessons = []
    with open(LESSONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if period and not entry.get('date', '').startswith(period):
                    continue
                lessons.append(entry)
            except json.JSONDecodeError:
                pass
    return lessons

def generate_report(lessons, period=None):
    today = datetime.now().strftime('%Y-%m-%d')
    period_label = period or 'All Time'

    if not lessons:
        return (
            f"# Learning Report — {period_label}\n"
            f"Generated: {today}\n\n"
            "No lessons logged yet. Use `/lesson` to start capturing learnings.\n"
        )

    by_category   = defaultdict(list)
    by_month       = defaultdict(int)
    trigger_counts = Counter()

    for l in lessons:
        by_category[l.get('category', 'general')].append(l)
        by_month[l.get('date', '')[:7]] += 1
        trigger_counts[l.get('trigger', 'manual')] += 1

    sorted_cats = sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)

    lines = [
        f"# Learning Report — {period_label}",
        f"Generated: {today}  |  Total lessons: **{len(lessons)}**",
        f"Auto-captured: {trigger_counts.get('auto',0)} + {trigger_counts.get('hook',0)}  "
        f"|  Manual: {trigger_counts.get('manual',0)}",
        "",
        "---",
        "",
        "## Lessons by Category",
        "",
        "| Category | Count | Signal |",
        "|----------|-------|--------|",
    ]

    for cat, cat_lessons in sorted_cats:
        bar = '█' * len(cat_lessons)
        lines.append(f"| {cat.title()} | {len(cat_lessons)} | {bar} |")

    lines += ["", "---", ""]

    # Monthly trend
    if len(by_month) > 1:
        lines += ["## Monthly Trend", ""]
        for month in sorted(by_month):
            lines.append(f"- **{month}**: {by_month[month]} lessons")
        lines += ["", "---", ""]

    # Detail per category
    lines += ["## Full Lesson Log", ""]
    for cat, cat_lessons in sorted_cats:
        lines.append(f"### {cat.title()} ({len(cat_lessons)})")
        lines.append("")
        for l in sorted(cat_lessons, key=lambda x: x.get('date', '')):
            date    = l.get('date', '?')
            trigger = l.get('trigger', 'manual')
            lesson  = l.get('lesson', '')
            why     = l.get('why', '')
            icon    = '🤖' if trigger in ('auto', 'hook') else '✍️'
            lines.append(f"**[{date}]** {icon}")
            lines.append(f"- **Lesson:** {lesson}")
            if why:
                lines.append(f"- **Why:** {why}")
            lines.append("")

    # High-frequency warning
    high_freq = [(c, ls) for c, ls in sorted_cats if len(ls) >= 3]
    if high_freq:
        lines += [
            "---", "",
            "## ⚠️ Repeated Patterns (3+ lessons in same category)",
            "",
            "These categories need permanent rule changes in `lessons-learned.md`:",
            "",
        ]
        for cat, ls in high_freq:
            lines.append(f"- **{cat.title()}**: {len(ls)} lessons — consider adding a hard rule or hook")

    lines += [
        "", "---", "",
        "## Action Items",
        "",
        "- [ ] Move high-frequency lessons into `~/.claude/docs/lessons-learned.md` as permanent rules",
        "- [ ] Delete lessons Claude now does correctly without being reminded",
        "- [ ] If 3+ lessons in same category → add a hook to enforce it automatically",
        "- [ ] Push updated files to GitHub so all devices stay in sync",
    ]

    return '\n'.join(lines)

def main():
    args   = [a for a in sys.argv[1:] if a != '--stdout']
    stdout = '--stdout' in sys.argv
    period = args[0] if args else None

    lessons = load_lessons(period)
    report  = generate_report(lessons, period)

    print(report)

    if not stdout:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        fname    = f"learning-report-{period or datetime.now().strftime('%Y-%m')}.md"
        filepath = os.path.join(REPORTS_DIR, fname)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n---\nReport saved: {filepath}")

if __name__ == '__main__':
    main()
