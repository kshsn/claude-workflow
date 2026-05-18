#!/usr/bin/env python3
"""SessionStart hook — logs session start and injects auto-lesson instructions."""
import sys, json, datetime, os

LOG_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'sessions.log')

def main():
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] SESSION START\n")
    except Exception:
        pass

    # Inject auto-lesson rules into every session context
    print(
        "SESSION RULES:\n"
        "1. Read the project CLAUDE.md and .claude/ folder before doing anything else.\n"
        "2. AUTO-LESSON: Whenever you correct a mistake THIS session, call /lesson immediately.\n"
        "3. AUTO-LESSON: If the user corrects you, call /lesson after fixing the issue.\n"
        "4. Run /compact when context reaches ~50% usage.\n"
        "5. Commit one file at a time — never git add ."
    )

if __name__ == '__main__':
    main()
