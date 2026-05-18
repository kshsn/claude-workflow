#!/usr/bin/env python3
"""Stop hook — logs session completion timestamp and stop reason."""
import sys, json, datetime, os

LOG_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'sessions.log')

def main():
    try:
        data = json.load(sys.stdin)
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reason = data.get('stop_reason', 'unknown')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] STOP — reason: {reason}\n")
    except Exception:
        pass

if __name__ == '__main__':
    main()
