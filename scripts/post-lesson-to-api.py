#!/usr/bin/env python3
"""
post-lesson-to-api.py
Called by log-lesson.py to sync a lesson to the VPS database.
Falls back silently if VPS is unreachable.
"""
import json, os, sys, socket
from urllib.request import urlopen, Request
from urllib.error import URLError

LOCAL_CFG = os.path.join(os.path.expanduser('~'), '.claude', 'lessons-api.json')

def post_lesson(lesson_entry: dict) -> bool:
    if not os.path.exists(LOCAL_CFG):
        return False
    try:
        with open(LOCAL_CFG) as f:
            cfg = json.load(f)
        data = json.dumps(lesson_entry).encode('utf-8')
        req  = Request(
            f"{cfg['api_url']}/lessons",
            data=data,
            headers={
                'Content-Type': 'application/json',
                'x-api-key':    cfg['api_key'],
            },
            method='POST'
        )
        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except (URLError, OSError, KeyError):
        return False  # Silent fail — VPS unreachable is acceptable

if __name__ == '__main__':
    entry = json.loads(sys.stdin.read())
    ok = post_lesson(entry)
    print("VPS sync:", "OK" if ok else "skipped (offline)")
