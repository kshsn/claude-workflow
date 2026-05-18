#!/usr/bin/env python3
"""
setup-vps-config.py
Run once on a new device to connect it to the VPS lessons API.

Usage: python setup-vps-config.py
Saves config to ~/.claude/lessons-api.json
"""
import json, os, sys
from urllib.request import urlopen, Request
from urllib.error import URLError

LOCAL_CFG = os.path.join(os.path.expanduser('~'), '.claude', 'lessons-api.json')

def test_connection(api_url, api_key):
    try:
        req = Request(f"{api_url}/health", headers={'x-api-key': api_key})
        with urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            return True, data
    except Exception as e:
        return False, str(e)

def main():
    print("\n=== VPS Lessons API — New Device Setup ===")
    print("Connect this device to your central lessons database.")
    print("(Copy these values from ~/.claude/lessons-api.json on your primary device)\n")

    if os.path.exists(LOCAL_CFG):
        with open(LOCAL_CFG) as f:
            existing = json.load(f)
        print(f"Existing config found: {existing.get('api_url', '?')}")
        overwrite = input("Overwrite? [y/N]: ").strip().lower()
        if overwrite != 'y':
            print("Aborted — existing config kept.")
            return

    api_url = input("API URL (e.g. http://89.116.236.22:4000): ").strip().rstrip('/')
    api_key = input("API key (starts with claude_lrn_): ").strip()

    if not api_url or not api_key:
        print("Error: both API URL and key are required.")
        sys.exit(1)

    print("\nTesting connection...")
    ok, result = test_connection(api_url, api_key)
    if ok:
        print(f"Connected! API responded: {result}")
    else:
        print(f"Warning: connection failed — {result}")
        proceed = input("Save config anyway? [y/N]: ").strip().lower()
        if proceed != 'y':
            print("Aborted.")
            return

    cfg = {"api_url": api_url, "api_key": api_key}
    os.makedirs(os.path.dirname(LOCAL_CFG), exist_ok=True)
    with open(LOCAL_CFG, 'w') as f:
        json.dump(cfg, f, indent=2)

    print(f"\nConfig saved to {LOCAL_CFG}")
    print("This device will now sync lessons to and recall from the VPS.")
    print("Run: python recall-lessons.py  — to verify")

if __name__ == '__main__':
    main()
