---
description: Rules for API routes, controllers, and backend endpoint code
paths: ["src/api/**", "*.route.ts", "*.controller.ts", "routes/**", "api/**", "*.route.js"]
---

# API Development Rules

## Input Validation
- Validate ALL user input at the route boundary before passing to services
- Use a schema library (Zod, Joi, or Yup) — never validate manually with if-chains
- Return 400 with a clear, specific error message for invalid input — never 500
- Strip unknown fields from request bodies — never pass raw req.body to the database

## Response Standards
- Always return typed responses — never return `any` or untyped objects
- Use a consistent envelope: `{ data: ..., error: null }` or `{ data: null, error: "message" }`
- Never expose internal error messages, stack traces, or database errors to clients
- Set appropriate HTTP status codes — 200/201 success, 400 bad input, 401 unauth, 403 forbidden, 404 not found

## Authentication & Authorization
- Every protected route must verify authentication via middleware — not inline
- Never trust client-provided user IDs — always derive identity from the verified auth token
- Check authorization (can this user access THIS resource?) separately from authentication

## Database
- Never construct queries via string concatenation — use parameterized queries or ORM methods
- Never return raw database rows — map to response DTOs before sending
- Wrap multi-step operations in database transactions
- Index foreign keys and frequently queried columns
