# Security Rules

Apply to every project. Non-negotiable.

---

## Secrets Management
- NEVER hardcode API keys, tokens, passwords, or connection strings in code
- Store secrets in `.env` — add `.env` to `.gitignore` immediately at project start
- Provide `.env.example` with placeholder values (e.g. `DATABASE_URL=postgres://user:pass@host/db`)
- Reference in code via: `process.env.API_KEY` (Node) or `os.environ["KEY"]` (Python)
- If a secret is accidentally committed: **rotate it immediately**, then remove from git history

---

## OWASP Top 10 Checklist (verify before every deploy)
- [ ] **Injection:** All queries use parameterized statements or ORM — no string concatenation
- [ ] **Broken Auth:** JWT stored in httpOnly cookies, not localStorage
- [ ] **Sensitive Data:** HTTPS everywhere, no PII or tokens in logs
- [ ] **XSS:** All user-generated content sanitized before rendering in HTML
- [ ] **Broken Access Control:** Every protected route checks authentication AND authorization
- [ ] **Security Misconfiguration:** Debug mode off, no default credentials, headers set
- [ ] **Vulnerable Components:** Run `npm audit` — fix Critical and High before deploy
- [ ] **Insecure Deserialization:** Validate all deserialized/parsed data at boundaries
- [ ] **Logging & Monitoring:** Errors logged, sensitive data never logged
- [ ] **SSRF:** Validate and allowlist all server-side URL inputs

---

## Input Validation
- Validate at system boundaries only: user input, external API responses, file uploads
- Trust internal code — don't add redundant validation between your own services
- Reject early with a clear 400 error — never silently discard invalid input

---

## Dependency Security
- Run `npm audit` before every release — fix Critical/High severity issues
- Pin exact versions for security-sensitive packages in package.json
- Review changelog before upgrading auth, crypto, or session packages

---

## Git Security
- `.env` in `.gitignore` — check this before first commit
- Never commit: private keys, certificates, database dumps, API credentials
- Use `git diff --staged` to review what you're about to commit
