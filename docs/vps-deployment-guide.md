# ClinicFlow — VPS Deployment Guide

**Target**: Oracle A1Flex (ARM64) · Docker · Portainer · Cloudflare Tunnel  
**Domain**: `demoerp.clinicflow.vet`  
**Odoo**: 19.0 CE · PostgreSQL 15

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Oracle A1Flex VPS | Ubuntu 22.04 recommended |
| Docker + Docker Compose | Installed (Portainer bootstraps this) |
| Portainer CE | Running and accessible |
| Cloudflare Tunnel | `cloudflared` installed and authenticated |
| GitHub access | Repo cloned on VPS |
| DNS | `demoerp.clinicflow.vet` CNAME → your CF tunnel (auto-created by cloudflared) |

> **ARM64 Note**: `odoo:19.0` on Docker Hub publishes a multi-arch manifest including `linux/arm64`. No custom image needed.

---

## Step 1 — Deploy the Portainer Git Stack

This method securely deploys the application directly from GitHub without needing to manually SSH and clone the repository. It also uses CLI flags for Odoo, so no `odoo.conf` file needs to be manually created.

1. In Portainer, go to **Stacks** → **Add Stack**.
2. Select **Repository** (instead of Web editor).
3. Enter your GitHub Repository URL (e.g., `https://github.com/YOUR_ORG/clinicflow-on-odoo.git`).
4. *If the repo is private*, enable Authentication and provide your GitHub Personal Access Token (PAT).
5. Set the **Compose path** to `docker-compose.prod.yml`.
6. Set the following **Environment variables**:

| Variable | Value |
|---|---|
| `DB_PASSWORD` | your strong database password |
| `MASTER_PASSWORD` | your Odoo master/admin password |
| `CF_TUNNEL_TOKEN` | your Cloudflare Tunnel token (if managing tunnel via Portainer) |

7. **Optional**: Enable "Automatic updates" so Portainer can poll GitHub and automatically redeploy when you push new code (or you can trigger it manually in the UI).
8. Click **Deploy the stack**.

---

## Step 2 — Initialize the Database

Run once after the containers are up. Since Portainer manages the volume, you can use the Portainer Console or SSH:

```bash
# Install all ClinicFlow modules and create the DB
docker exec odoo_clinicflow_prod odoo \
  -d clinicflow \
  -i clinicflow_core,clinicflow_patient,clinicflow_clinical,\
clinicflow_billing,clinicflow_ai,clinicflow_outreach \
  --stop-after-init

# Optional: run seed data (requires SSH)
cat /data/compose/*/seed_data.py | docker exec -i odoo_clinicflow_prod \
  odoo shell -d clinicflow --no-http
```

---

## Step 3 — Configure Cloudflare Tunnel

### If using `cloudflared` as a system service:

```bash
# Authenticate (run once)
cloudflared tunnel login

# Create the tunnel
cloudflared tunnel create clinicflow-prod

# Write config
cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: clinicflow-prod
credentials-file: /root/.cloudflared/<PASTE_TUNNEL_UUID_HERE>.json

ingress:
  - hostname: demoerp.clinicflow.vet
    service: http://odoo_clinicflow_prod:8069
  - service: http_status:404
EOF

# Create DNS CNAME in Cloudflare automatically
cloudflared tunnel route dns clinicflow-prod demoerp.clinicflow.vet

# Install and start as a system service
cloudflared service install
sudo systemctl enable --now cloudflared
```

### If using Portainer to run cloudflared as a container:

Add this service to your stack (or as a separate stack):

```yaml
cloudflared:
  image: cloudflare/cloudflared:latest
  container_name: cloudflared_clinicflow
  restart: always
  command: tunnel --no-autoupdate run
  environment:
    - TUNNEL_TOKEN=YOUR_CF_TUNNEL_TOKEN_HERE
  networks:
    - clinicflow-net
```

Get the token from Cloudflare Zero Trust → Tunnels → your tunnel → **Configure → Docker**.

> **This is the recommended approach for Portainer** — no SSH needed, fully managed via the UI.

---

## Step 4 — Post-Deploy Configuration (Manual in Odoo UI)

After first login at `https://demoerp.clinicflow.vet`:

1. **Set `web.base.url`**  
   Settings → Technical → Parameters → System Parameters  
   Find `web.base.url` → set to `https://demoerp.clinicflow.vet`

2. **Create the clinic company**  
   Settings → Companies → New  
   Set name, logo, currency, timezone, address.

3. **Set the admin password for the Odoo user**  
   Settings → Users → Administrator → Change Password

---

## Step 5 — Keeping the Code Updated

Because you are using Portainer's Git Stack feature:

1. In Portainer, go to your Stack.
2. Click **Pull and redeploy**. Portainer will fetch the latest code from GitHub and recreate the containers.
3. Then, upgrade all ClinicFlow modules via the console/SSH:

```bash
docker exec odoo_clinicflow_prod odoo \
  -d clinicflow \
  -u clinicflow_core,clinicflow_patient,clinicflow_clinical,\
clinicflow_billing,clinicflow_ai,clinicflow_outreach \
  --stop-after-init

docker restart odoo_clinicflow_prod
```

---

## Backup

Schedule these via cron (`crontab -e`):

```bash
# Daily DB backup at 2am
0 2 * * * docker exec postgres_clinicflow pg_dump -U odoo clinicflow \
  | gzip > /opt/backups/clinicflow_$(date +\%Y\%m\%d).sql.gz

# Keep last 14 days
0 3 * * * find /opt/backups -name "*.sql.gz" -mtime +14 -delete
```

```bash
# Filestore backup
0 4 * * * docker run --rm \
  -v odoo-clinicflow-prod-data:/data \
  -v /opt/backups:/backup \
  busybox tar czf /backup/filestore_$(date +\%Y\%m\%d).tar.gz /data
```

---

## Firewall (Oracle Security List)

Only **SSH (22)** needs to be open inbound. Cloudflare Tunnel establishes an **outbound** connection — no inbound ports needed for Odoo.

```bash
# Verify nothing else is exposed
sudo ufw status
# Should show only 22/tcp open
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Blank page / CSS broken after CF Tunnel | Ensure `--proxy-mode` is in the `command:` list in `docker-compose.prod.yml` |
| 502 Bad Gateway | Check container is running: `docker ps` |
| Module not found | Verify Portainer bind-mounted `.` to `/mnt/extra-addons` correctly |
| ARM64 image pull fails | Run `docker pull --platform linux/arm64 odoo:19.0` to confirm |
| Session keeps expiring | Set `web.base.url` to the correct HTTPS domain in System Parameters |
