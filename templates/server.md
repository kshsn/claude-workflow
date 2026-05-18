# Deployment — Server Config

---

## VPS Details
| Field             | Value |
|-------------------|-------|
| Host              |       |
| User              |       |
| App Path          | /var/www/<project> |
| PM2 Process Name  |       |
| Production URL    |       |
| Node Version      |       |

---

## Deploy Commands
```bash
# 1. Build locally
npm run build

# 2. Sync to server (excludes node_modules and .git)
rsync -avz --exclude node_modules --exclude .git ./dist user@host:/var/www/<project>

# 3. Install & restart on server
ssh user@host "cd /var/www/<project> && npm install --production && pm2 restart <process-name>"

# 4. Health check
curl -f https://<production-url>/health
```

---

## Required Environment Variables
<!-- List keys only — never commit values -->
```
DATABASE_URL=
NODE_ENV=production
PORT=
JWT_SECRET=
```

---

## Nginx Config Location
```
/etc/nginx/sites-available/<project>
```

---

## SSL
- [ ] SSL certificate installed (Let's Encrypt / Certbot)
- [ ] Auto-renewal configured

---

## Notes
<!-- Server-specific quirks, firewall rules, reverse proxy setup, etc. -->
