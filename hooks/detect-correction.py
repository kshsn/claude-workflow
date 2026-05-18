#!/usr/bin/env python3
"""
UserPromptSubmit hook — detects corrections and:
1. Auto-logs a draft lesson entry immediately (VPS + local)
2. Injects a reminder so Claude creates a refined /lesson entry

This guarantees corrections are never silently lost.
"""
import sys, json, re, os, subprocess

CORRECTION_SIGNALS = [
    r'\b(no,?\s+don\'?t|don\'?t do that|stop doing|never do)\b',
    r'\b(that\'?s wrong|that\'?s incorrect|that\'?s not right|wrong approach)\b',
    r'\b(actually[,\s]+you should|actually[,\s]+it should)\b',
    r'\b(you missed|you forgot|you broke|you messed)\b',
    r'\b(undo that|revert that|that was a mistake)\b',
    r'\b(i said|i told you|i already said)\b',
    r'\bno[,\s]+(use|do|run|put|add|write)\b',
]

SCRIPT_DIR = os.path.join(os.path.expanduser('~'), '.claude', 'scripts')

def is_correction(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in CORRECTION_SIGNALS)

def auto_log_draft(message: str) -> None:
    """Immediately log a draft correction entry so it's never lost."""
    draft_lesson = f"[AUTO] Correction detected: {message[:120].strip()}"
    try:
        script = os.path.join(SCRIPT_DIR, 'log-lesson.py')
        subprocess.run(
            ['python', script,
             '--category', 'general',
             '--lesson', draft_lesson,
             '--why', 'Auto-captured at correction time — Claude will refine this with /lesson',
             '--trigger', 'auto-hook'],
            timeout=8, capture_output=True
        )
    except Exception:
        pass

def main():
    try:
        data    = json.load(sys.stdin)
        message = data.get('message', '') or data.get('prompt', '')

        if is_correction(message):
            auto_log_draft(message)

            injection = (
                "\n\n[AUTO-LESSON TRIGGER: A correction was detected and a draft entry was "
                "auto-logged. After fixing the issue, call /lesson immediately with the specific "
                "lesson text and root cause. This replaces the draft with a precise entry.]"
            )
            print(json.dumps({"injection": injection}))
        else:
            print(json.dumps({}))
    except Exception:
        print(json.dumps({}))

if __name__ == '__main__':
    main()
