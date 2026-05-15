# Deployment — {{PROJECT_NAME}}

## Hostinger VPS

| Field | Value |
|-------|-------|
| Host | {{VPS_IP_OR_HOSTNAME}} |
| SSH User | {{SSH_USER}} |
| App Path | /var/www/{{PROJECT_NAME}} |
| PM2 Process | {{PROJECT_NAME}} |
| Production URL | https://{{DOMAIN}} |
| Node Version | {{NODE_VERSION}} |

## Environment Variables (production)
```
NODE_ENV=production
DATABASE_URL=
PORT=3000
```

## Deploy Commands
```bash
# Build locally
npm run build

# Sync to server
rsync -avz --exclude node_modules --exclude .git ./dist {{SSH_USER}}@{{VPS_IP}}:/var/www/{{PROJECT_NAME}}

# Restart on server
ssh {{SSH_USER}}@{{VPS_IP}} "cd /var/www/{{PROJECT_NAME}} && npm install --production && pm2 restart {{PROJECT_NAME}}"

# Health check
curl https://{{DOMAIN}}/health
```

## First-Time Server Setup
```bash
# On the VPS (run once)
npm install -g pm2
mkdir -p /var/www/{{PROJECT_NAME}}
pm2 startup
```
