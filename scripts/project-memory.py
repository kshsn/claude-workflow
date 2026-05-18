#!/usr/bin/env python3
"""
project-memory.py — Cloud-backed per-project memory via VPS API.

Usage:
  python project-memory.py read   --project <name>
  python project-memory.py add    --project <name> --section <section> --entry <text>
  python project-memory.py forget --project <name> --keyword <word>
  python project-memory.py delete --project <name> --id <id>

Sections: Decisions | Active Work | Blockers | Key Facts | Session Log | Notes
Config:   ~/.claude/lessons-api.json
"""
import argparse, json, os, sys
from urllib.request import urlopen, Request
from urllib.error import URLError

LOCAL_CFG = os.path.join(os.path.expanduser('~'), '.claude', 'lessons-api.json')

SECTIONS = ['Decisions', 'Active Work', 'Blockers', 'Key Facts', 'Session Log', 'Notes']

def load_cfg():
    if not os.path.exists(LOCAL_CFG):
        print("Error: ~/.claude/lessons-api.json not found. Run setup-vps-config.py first.")
        sys.exit(1)
    with open(LOCAL_CFG) as f:
        return json.load(f)

def api(cfg, method, path, body=None):
    url  = f"{cfg['api_url']}{path}"
    data = json.dumps(body).encode() if body else None
    req  = Request(url, data=data, headers={
        'x-api-key':    cfg['api_key'],
        'Content-Type': 'application/json',
    }, method=method)
    try:
        with urlopen(req, timeout=6) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"VPS error: {e}")
        sys.exit(1)

def cmd_read(cfg, project):
    data    = api(cfg, 'GET', f'/memory/{project}')
    entries = data.get('entries', [])
    if not entries:
        print(f"No memory found for project '{project}'.")
        print("Add entries with: python project-memory.py add --project <name> --entry <text>")
        return

    from collections import defaultdict
    by_section = defaultdict(list)
    for e in entries:
        by_section[e.get('section', 'Notes')].append(e)

    print(f"\n=== PROJECT MEMORY — {project} ({len(entries)} entries) ===\n")
    for section in SECTIONS:
        items = by_section.get(section, [])
        if not items:
            continue
        print(f"[{section.upper()}]")
        for item in items:
            date = str(item.get('created_at', ''))[:10]
            print(f"  #{item['id']}  {date}  {item['entry']}")
            if item.get('device'):
                print(f"              [{item['device']}]")
        print()

    # Print any unlisted sections
    for section, items in by_section.items():
        if section not in SECTIONS:
            print(f"[{section.upper()}]")
            for item in items:
                date = str(item.get('created_at', ''))[:10]
                print(f"  #{item['id']}  {date}  {item['entry']}")
            print()

def cmd_add(cfg, project, section, entry, device='windows-main'):
    data = api(cfg, 'POST', '/memory', {
        'project': project,
        'section': section,
        'entry':   entry,
        'device':  device,
    })
    mem = data.get('memory', {})
    print(f"Saved to [{section}] #{mem.get('id','?')}: {entry}")

def cmd_forget(cfg, project, keyword):
    data = api(cfg, 'DELETE', f'/memory/{project}/keyword/{keyword}')
    removed = data.get('removed', 0)
    print(f"Removed {removed} entry/entries matching '{keyword}' from '{project}'")

def cmd_delete(cfg, project, entry_id):
    api(cfg, 'DELETE', f'/memory/{entry_id}')
    print(f"Deleted entry #{entry_id}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['read', 'add', 'forget', 'delete'])
    parser.add_argument('--project',  required=True)
    parser.add_argument('--section',  default='Notes')
    parser.add_argument('--entry',    default='')
    parser.add_argument('--keyword',  default='')
    parser.add_argument('--id',       default='')
    parser.add_argument('--device',   default='windows-main')
    args = parser.parse_args()

    cfg = load_cfg()

    if args.cmd == 'read':
        cmd_read(cfg, args.project)
    elif args.cmd == 'add':
        if not args.entry:
            print("Error: --entry is required")
            sys.exit(1)
        section = args.section.title() if args.section.lower() in [s.lower() for s in SECTIONS] else args.section
        cmd_add(cfg, args.project, section, args.entry, args.device)
    elif args.cmd == 'forget':
        if not args.keyword:
            print("Error: --keyword is required")
            sys.exit(1)
        cmd_forget(cfg, args.project, args.keyword)
    elif args.cmd == 'delete':
        if not args.id:
            print("Error: --id is required")
            sys.exit(1)
        cmd_delete(cfg, args.project, args.id)

if __name__ == '__main__':
    main()
