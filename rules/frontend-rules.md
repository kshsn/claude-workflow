---
description: Rules for React/React Native components, pages, and UI code
paths: ["src/components/**", "src/pages/**", "src/app/**", "src/screens/**", "*.tsx", "*.jsx"]
---

# Frontend Development Rules

## Component Design
- One component per file — no exceptions
- All props must be typed with a TypeScript interface or type
- No inline styles — use Tailwind classes, CSS modules, or NativeWind
- Extract reusable logic into custom hooks (`useAuth`, `useForm`, etc.)

## Security
- Never use `dangerouslySetInnerHTML` unless content is explicitly sanitized first
- Never store tokens, passwords, or sensitive data in localStorage — use httpOnly cookies
- Sanitize all user-generated content before rendering

## State & Data
- Keep state as local as possible — lift only when two+ components need it
- Never fetch data directly in components — use custom hooks or a dedicated data layer
- Every async operation requires loading and error states — never show blank screens

## Accessibility (a11y)
- Every interactive element needs an accessible label (`aria-label` or visible text)
- Images need descriptive `alt` text (use empty `alt=""` for decorative images only)
- All form inputs need associated `<label>` elements
- Color alone must not convey meaning — add icons or text

## React Native Specific
- Use `npx expo install <package>` — never `npm install` for Expo projects
- Use NativeWind for styling — avoid StyleSheet.create for layout-heavy components
