#!/usr/bin/env python3
"""Stop hook — logs session end and prompts Claude to review lessons before closing."""
import sys, json, datetime, os

LOG_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'sessions.log')

def main():
    try:
        data   = json.load(sys.stdin)
        reason = data.get('stop_reason', 'unknown')
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] STOP — reason: {reason}\n")
    except Exception:
        pass

    print(
        "SESSION ENDING — Before closing:\n"
        "1. Did you learn anything new or fix a mistake this session?\n"
        "   If YES → call /lesson now to log it before the session closes.\n"
        "2. Did you complete a phase or epic?\n"
        "   If YES → commit CLAUDE.md with the updated phase status.\n"
        "Run /learning-report to see all lessons captured so far."
    )

if __name__ == '__main__':
    main()
