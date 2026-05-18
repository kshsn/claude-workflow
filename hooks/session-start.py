#!/usr/bin/env python3
"""SessionStart hook — logs session start and reminds Claude to read project CLAUDE.md."""
import sys, json, datetime, os

LOG_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'sessions.log')

def main():
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] SESSION START\n")
        # Print reminder into Claude's context
        print("REMINDER: Read the project CLAUDE.md and .claude/ folder before doing anything else.")
    except Exception:
        pass

if __name__ == '__main__':
    main()
