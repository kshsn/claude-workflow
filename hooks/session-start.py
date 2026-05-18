#!/usr/bin/env python3
"""
SessionStart hook — prints session rules and injects recent lessons from VPS.
Claude starts each session already aware of the most recent mistakes.
"""
import sys, json, datetime, os
from urllib.request import urlopen, Request
from urllib.error import URLError

LOG_FILE  = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'sessions.log')
LOCAL_CFG = os.path.join(os.path.expanduser('~'), '.claude', 'lessons-api.json')

RULES = (
    "SESSION RULES:\n"
    "1. Read the project CLAUDE.md and .claude/ folder before doing anything else.\n"
    "2. AUTO-LESSON: Whenever you correct a mistake THIS session, call /lesson immediately.\n"
    "3. AUTO-LESSON: If the user corrects you, call /lesson after fixing the issue.\n"
    "4. Run /compact when context reaches ~50% usage.\n"
    "5. Commit one file at a time — never git add ."
)

def fetch_recent_lessons(limit=5):
    if not os.path.exists(LOCAL_CFG):
        return []
    try:
        with open(LOCAL_CFG) as f:
            cfg = json.load(f)
        url = f"{cfg['api_url']}/lessons?limit={limit}"
        req = Request(url, headers={'x-api-key': cfg['api_key']})
        with urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            lessons = data if isinstance(data, list) else data.get('lessons', [])
            return lessons[-limit:]
    except Exception:
        return []

def log_session_start():
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] SESSION START\n")
    except Exception:
        pass

def main():
    log_session_start()
    print(RULES)

    recent = fetch_recent_lessons(limit=5)
    if recent:
        lines = ["\nRECENT LESSONS (auto-loaded from VPS — avoid repeating these):"]
        for item in recent:
            cat    = item.get('category', 'general')
            lesson = item.get('lesson', '')
            date   = str(item.get('date', ''))[:10]
            lines.append(f"  [{cat}] {date}: {lesson}")
        print('\n'.join(lines))

if __name__ == '__main__':
    main()
