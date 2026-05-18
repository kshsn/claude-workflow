#!/usr/bin/env python3
"""PreToolUse hook — blocks secrets from being written to any file."""
import sys, json, re

SECRET_PATTERNS = [
    r'sk-[A-Za-z0-9]{32,}',
    r'github_pat_[A-Za-z0-9_]{36,}',
    r'ghp_[A-Za-z0-9]{36,}',
    r'xoxb-[A-Za-z0-9\-]{40,}',
    r'AKIA[0-9A-Z]{16}',
    r'(?i)(api[_-]?key)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{20,}',
    r'(?i)(secret[_-]?key)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}',
    r'(?i)(password|passwd)\s*[:=]\s*["\']?[^\s"\']{8,}',
    r'(?i)(access[_-]?token|auth[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9_\-\.]{16,}',
]

SAFE_SUFFIXES = ['.example', '.sample', '.template', '.md']

def main():
    try:
        data = json.load(sys.stdin)
        tool_input = data.get('tool_input', {})
        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '')

        for suffix in SAFE_SUFFIXES:
            if file_path.endswith(suffix):
                print(json.dumps({"decision": "approve"}))
                return

        for pattern in SECRET_PATTERNS:
            if re.search(pattern, content):
                print(json.dumps({
                    "decision": "block",
                    "reason": (
                        f"Secret detected in {file_path}. "
                        "Store secrets in .env (add to .gitignore) and reference via process.env.KEY."
                    )
                }))
                return

        print(json.dumps({"decision": "approve"}))
    except Exception:
        print(json.dumps({"decision": "approve"}))

if __name__ == '__main__':
    main()
