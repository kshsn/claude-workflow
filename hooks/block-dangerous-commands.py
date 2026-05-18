#!/usr/bin/env python3
"""PreToolUse hook — blocks destructive shell commands."""
import sys, json, re

SAFE_PATTERNS = [
    r'rm\s+-rf\s+(node_modules|\.next|dist|build|\.expo|coverage)',
]

DANGEROUS_PATTERNS = [
    (r'\brm\s+-rf\s+/(?:$|\s|etc|usr|var|boot|bin|sbin|lib|proc|sys|dev)', "rm -rf on system root or critical directory is blocked"),
    (r'git\s+push\s+.*--force.*(main|master)', "Force push to main/master is blocked"),
    (r'\bDROP\s+(DATABASE|TABLE)\b', "SQL DROP DATABASE/TABLE is blocked"),
    (r'git\s+reset\s+--hard\s+HEAD~[2-9]', "Hard reset of multiple commits requires explicit confirmation"),
    (r'\bdel\s+/[sq].*[a-zA-Z]:\\\\?$', "Bulk delete from drive root is blocked"),
    (r'format\s+[a-zA-Z]:', "Drive format command is blocked"),
]

def main():
    try:
        data = json.load(sys.stdin)
        command = data.get('tool_input', {}).get('command', '')

        for safe in SAFE_PATTERNS:
            if re.search(safe, command, re.IGNORECASE):
                print(json.dumps({"decision": "approve"}))
                return

        for pattern, reason in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                print(json.dumps({"decision": "block", "reason": reason}))
                return

        print(json.dumps({"decision": "approve"}))
    except Exception:
        print(json.dumps({"decision": "approve"}))

if __name__ == '__main__':
    main()
