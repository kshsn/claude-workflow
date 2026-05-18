#!/usr/bin/env python3
"""
SessionStart hook — injects:
1. Session rules
2. Project memory from VPS (detected from cwd project name)
3. Recent global lessons from VPS
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

def load_cfg():
    if not os.path.exists(LOCAL_CFG):
        return None
    try:
        with open(LOCAL_CFG) as f:
            return json.load(f)
    except Exception:
        return None

def api_get(cfg, path):
    try:
        req = Request(f"{cfg['api_url']}{path}", headers={'x-api-key': cfg['api_key']})
        with urlopen(req, timeout=4) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

def detect_project():
    """Detect project from CLAUDE.md → git remote → package.json → folder name."""
    import re, subprocess
    cwd = os.getcwd()
    home = os.path.expanduser('~')

    # 1. CLAUDE.md first heading
    claude_md = os.path.join(cwd, 'CLAUDE.md')
    if os.path.exists(claude_md):
        try:
            with open(claude_md, encoding='utf-8', errors='ignore') as f:
                for line in f:
                    m = re.match(r'^#\s+(.+?)(?:\s+[-—].*)?$', line.strip())
                    if m:
                        name = m.group(1).strip().lower().replace(' ', '-')
                        if name not in ('claude', 'claude-global-workflow', 'global'):
                            return name
        except Exception:
            pass

    # 2. git remote origin
    try:
        out = subprocess.check_output(
            ['git', 'remote', 'get-url', 'origin'],
            stderr=subprocess.DEVNULL, cwd=cwd, timeout=4
        ).decode().strip()
        repo = re.split(r'[/:]', out)[-1].replace('.git', '')
        if repo:
            return repo
    except Exception:
        pass

    # 3. package.json
    pkg = os.path.join(cwd, 'package.json')
    if os.path.exists(pkg):
        try:
            with open(pkg) as f:
                name = json.load(f).get('name', '')
            if name:
                return name
        except Exception:
            pass

    # 4. folder name — skip home dir
    if cwd != home:
        return os.path.basename(cwd)

    return None

def fetch_project_memory(cfg, project):
    data = api_get(cfg, f'/memory/{project}')
    if not data:
        return []
    return data.get('entries', [])

def fetch_recent_lessons(cfg, limit=5):
    data = api_get(cfg, f'/lessons?limit={limit}')
    if not data:
        return []
    lessons = data if isinstance(data, list) else data.get('lessons', [])
    return lessons[-limit:]

def log_session_start(project):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] SESSION START — project: {project}\n")
    except Exception:
        pass

def main():
    project = detect_project()
    log_session_start(project)
    print(RULES)

    cfg = load_cfg()
    if not cfg:
        return

    # Project memory (only if a real project was detected)
    entries = fetch_project_memory(cfg, project) if project else []
    if entries:
        from collections import defaultdict
        by_section = defaultdict(list)
        for e in entries:
            by_section[e.get('section', 'Notes')].append(e['entry'])

        lines = [f"\nPROJECT MEMORY — {project} (from VPS):"]
        for section, items in by_section.items():
            lines.append(f"  [{section}]")
            for item in items:
                lines.append(f"    - {item}")
        print('\n'.join(lines))

    # Global lessons
    lessons = fetch_recent_lessons(cfg, limit=5)
    if lessons:
        lines = ["\nRECENT LESSONS (avoid repeating these):"]
        for item in lessons:
            cat    = item.get('category', 'general')
            lesson = item.get('lesson', '')
            date   = str(item.get('date', ''))[:10]
            lines.append(f"  [{cat}] {date}: {lesson}")
        print('\n'.join(lines))

if __name__ == '__main__':
    main()
