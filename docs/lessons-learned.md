# Lessons Learned

Rules from real past projects. Apply to every new project automatically.
Add new entries here whenever Claude makes a mistake that cost time.

---

## React Native / Expo — Dependencies
**Rule:** Always use `npx expo install <package>` — never `npm install`

- `npx expo install` picks the SDK-compatible version automatically
- `npm install` installs the latest version which often breaks the Expo build
- Applies to every package: reanimated, async-storage, navigation, etc.

**Source:** Smart Calculator project

---

## React Native / Expo — Build Timing
**Rule:** Run a test EAS build at the end of Phase 7 (Build), not Phase 9 (Deploy)

- Catches build errors early: missing babel plugins, Node version mismatches, broken deps
- Command: `eas build --profile preview --platform android --non-interactive`
- Fix all build errors before moving to Phase 8 (Testing)

**Source:** Smart Calculator project

---

## Figma MCP — Setup Timing
**Rule:** Set up the Figma MCP plugin before Phase 5 (Design) begins — not during it

Setup steps (do at project start):
1. Start WebSocket server:
   ```bash
   ~/.bun/bin/bun /usr/local/lib/node_modules/claude-talk-to-figma-mcp/dist/socket.js &
   ```
2. Open Figma Desktop → Plugins → Development → Claude Talk to Figma Plugin → Run → Connect
3. Confirm green "Connected" status before entering Phase 5

If plugin `code.js` is missing: download from `sonnylazuardi/cursor-talk-to-figma-mcp` on GitHub

**Source:** Smart Calculator project

---

## CLAUDE.md Hygiene
**Rule:** Keep files short and focused

- Global `~/.claude/CLAUDE.md` — under 100 lines (rules + references only)
- Project `CLAUDE.md` — under 200 lines (phase status + project-specific context)
- Long files get partially ignored by Claude — ruthlessly prune
- Update project CLAUDE.md after every completed phase

---

## General
**Rule:** Prefer vertical slices over horizontal phases during Build

- Bad: "do all DB first, then all API, then all UI"
- Good: ship one thin end-to-end feature per story (DB + API + UI together)
- Reason: delivers working software faster and surfaces integration issues early
