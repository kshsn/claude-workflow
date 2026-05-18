#!/usr/bin/env python3
"""
UserPromptSubmit hook — detects user corrections and injects a lesson-capture reminder.

When the user says something that signals Claude made a mistake, this hook appends
a silent instruction to the message so Claude knows to log a lesson after fixing it.
"""
import sys
import json
import re

CORRECTION_SIGNALS = [
    r'\b(no,?\s+don\'?t|don\'?t do that|stop doing|never do)\b',
    r'\b(that\'?s wrong|that\'?s incorrect|that\'?s not right|wrong approach)\b',
    r'\b(actually[,\s]+you should|actually[,\s]+it should)\b',
    r'\b(you missed|you forgot|you broke|you messed)\b',
    r'\b(undo that|revert that|that was a mistake)\b',
    r'\b(i said|i told you|i already said)\b',
    r'\bno[,\s]+(use|do|run|put|add|write)\b',
]

def is_correction(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in CORRECTION_SIGNALS)

def main():
    try:
        data    = json.load(sys.stdin)
        message = data.get('message', '') or data.get('prompt', '')

        if is_correction(message):
            # Inject a silent reminder Claude will see as part of the prompt context
            injection = (
                "\n\n[AUTO-LESSON TRIGGER: A correction was detected. "
                "After fixing the issue, immediately use /lesson to log what went wrong "
                "and why — include the category and root cause.]"
            )
            print(json.dumps({"injection": injection}))
        else:
            print(json.dumps({}))
    except Exception:
        print(json.dumps({}))

if __name__ == '__main__':
    main()
