#!/usr/bin/env python3
"""PostToolUse hook — auto-formats supported files after Write/Edit."""
import sys, json, subprocess, os

FORMATTERS = {
    '.ts':   ['npx', 'prettier', '--write'],
    '.tsx':  ['npx', 'prettier', '--write'],
    '.js':   ['npx', 'prettier', '--write'],
    '.jsx':  ['npx', 'prettier', '--write'],
    '.json': ['npx', 'prettier', '--write'],
    '.css':  ['npx', 'prettier', '--write'],
    '.py':   ['python', '-m', 'black', '--quiet'],
}

def main():
    try:
        data = json.load(sys.stdin)
        file_path = data.get('tool_input', {}).get('file_path', '')
        if not file_path or not os.path.exists(file_path):
            return
        ext = os.path.splitext(file_path)[1].lower()
        formatter = FORMATTERS.get(ext)
        if formatter:
            subprocess.run(formatter + [file_path], capture_output=True, timeout=15)
    except Exception:
        pass  # Never block on formatter errors

if __name__ == '__main__':
    main()
