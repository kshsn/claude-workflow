#!/usr/bin/env python3
"""
Utility: log-lesson.py
Called by /lesson command and hooks to append a lesson to the JSONL store.

Usage:
  python log-lesson.py --category hooks --lesson "Always X" --why "Y happened" --trigger auto
"""
import argparse
import json
import os
from datetime import datetime

LESSONS_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'logs', 'lessons.jsonl')

VALID_CATEGORIES = [
    'dependencies', 'build', 'hooks', 'testing',
    'deployment', 'git', 'security', 'design', 'workflow', 'general'
]

def log(category, lesson, why='', trigger='manual'):
    os.makedirs(os.path.dirname(LESSONS_FILE), exist_ok=True)
    now = datetime.now()
    entry = {
        'date':     now.strftime('%Y-%m-%d'),
        'time':     now.strftime('%H:%M:%S'),
        'category': category if category in VALID_CATEGORIES else 'general',
        'lesson':   lesson.strip(),
        'why':      why.strip(),
        'trigger':  trigger,   # manual | auto | hook
    }
    with open(LESSONS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return entry

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', default='general')
    parser.add_argument('--lesson',   required=True)
    parser.add_argument('--why',      default='')
    parser.add_argument('--trigger',  default='manual')
    args = parser.parse_args()
    entry = log(args.category, args.lesson, args.why, args.trigger)
    print(f"Lesson logged [{entry['category']}]: {entry['lesson']}")

if __name__ == '__main__':
    main()
