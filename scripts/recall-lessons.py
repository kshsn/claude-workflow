#!/usr/bin/env python3
"""
recall-lessons.py
Fetch and display lessons from VPS API. Falls back to local JSONL.

Usage:
  python recall-lessons.py                   # all lessons
  python recall-lessons.py hooks             # filter by category
  python recall-lessons.py --limit 10        # last 10 lessons
  python recall-lessons.py hooks --limit 5   # filtered + limited
"""
import json, os, sys
from urllib.request import urlopen, Request
from urllib.error import URLError
from collections import defaultdict

LOCAL_CFG   = os.path.join(os.path.expanduser('~'), '.claude', 'lessons-api.json')
LOCAL_JSONL = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'lessons.jsonl')

VALID_CATEGORIES = [
    'dependencies', 'build', 'hooks', 'testing',
    'deployment', 'git', 'security', 'design', 'workflow', 'general'
]

def fetch_from_vps(category=None, limit=None):
    if not os.path.exists(LOCAL_CFG):
        return None
    try:
        with open(LOCAL_CFG) as f:
            cfg = json.load(f)
        url = f"{cfg['api_url']}/lessons"
        params = []
        if category:
            params.append(f"category={category}")
        if limit:
            params.append(f"limit={limit}")
        if params:
            url += '?' + '&'.join(params)
        req = Request(url, headers={'x-api-key': cfg['api_key']})
        with urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            lessons = data if isinstance(data, list) else data.get('lessons', [])
            return lessons
    except Exception:
        return None

def fetch_local(category=None, limit=None):
    if not os.path.exists(LOCAL_JSONL):
        return []
    lessons = []
    with open(LOCAL_JSONL, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if not category or entry.get('category') == category:
                    lessons.append(entry)
            except Exception:
                pass
    return lessons[-limit:] if limit else lessons

def display(lessons, source):
    if not lessons:
        print(f"No lessons found (source: {source})")
        return

    by_cat = defaultdict(list)
    for item in lessons:
        by_cat[item.get('category', 'general')].append(item)

    print(f"\n=== LESSONS LEARNED — {len(lessons)} total [{source}] ===\n")
    for cat in sorted(by_cat):
        items = by_cat[cat]
        print(f"[{cat.upper()}] {len(items)} lesson(s)")
        for item in items:
            date   = str(item.get('date', '?'))[:10]  # trim ISO timestamp to YYYY-MM-DD
            lesson = item.get('lesson', '')
            why    = item.get('why', '')
            device = item.get('device', '')
            trigger = item.get('trigger', '')
            print(f"  {date}  {lesson}")
            if why:
                print(f"           Why: {why}")
            detail = ' | '.join(filter(None, [device, trigger]))
            if detail:
                print(f"           [{detail}]")
        print()

def main():
    args     = sys.argv[1:]
    category = None
    limit    = None

    # Parse: optional positional category, optional --limit N
    remaining = []
    i = 0
    while i < len(args):
        if args[i] == '--limit' and i + 1 < len(args):
            try:
                limit = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        else:
            remaining.append(args[i])
            i += 1

    if remaining:
        cat_arg = remaining[0].lower()
        if cat_arg in VALID_CATEGORIES:
            category = cat_arg
        else:
            print(f"Unknown category '{cat_arg}'. Valid: {', '.join(VALID_CATEGORIES)}")
            sys.exit(1)

    lessons = fetch_from_vps(category, limit)
    if lessons is not None:
        display(lessons, 'VPS database')
    else:
        print("VPS unreachable — falling back to local lessons.jsonl")
        lessons = fetch_local(category, limit)
        display(lessons, 'local JSONL')

if __name__ == '__main__':
    main()
