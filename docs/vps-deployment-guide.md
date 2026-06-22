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

## Step 1 — Clone the Repository on the VPS

```bash
sudo mkdir -p /opt/clinicflow
sudo chown $USER:$USER /opt/clinicflow
cd /opt/clinicflow

git clone https://github.com/YOUR_ORG/clinicflow-on-odoo.git .
```

All subsequent steps reference `/opt/clinicflow` as the working directory.

---

## Step 2 — Create the Production Config File

```bash
mkdir -p /opt/clinicflow/config
cat > /opt/clinicflow/config/odoo.prod.conf << 'EOF'
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = CHANGE_THIS_MASTER_PASSWORD
db_host = postgres_clinicflow
db_port = 5432
db_user = odoo
db_password = CHANGE_THIS_DB_PASSWORD
dbfilter = ^clinicflow$
proxy_mode = True
workers = 2
max_cron_threads = 1
limit_memory_hard = 1677721600
limit_memory_soft = 629145600
limit_request = 8192
limit_time_cpu = 60
limit_time_real = 120
EOF
```

> **`proxy_mode = True` is mandatory** when behind Cloudflare Tunnel — without it, session cookies and HTTPS redirects break.

---

## Step 3 — Deploy the Portainer Stack

In Portainer → **Stacks → Add Stack → Web editor**, paste the contents of `docker-compose.prod.yml` (see the companion file in this repo).

Set the following **environment variables** in Portainer's stack env section:

| Variable | Value |
|---|---|
| `DB_PASSWORD` | your strong database password |
| `MASTER_PASSWORD` | your Odoo master/admin password |
| `REPO_PATH` | `/opt/clinicflow` |

Click **Deploy the stack**.

---

## Step 4 — Initialize the Database

Run once after the containers are up:

```bash
# Install all ClinicFlow modules and create the DB
docker exec odoo_clinicflow_prod odoo \
  -d clinicflow \
  -i clinicflow_core,clinicflow_patient,clinicflow_clinical,\
clinicflow_billing,clinicflow_ai,clinicflow_outreach \
  --stop-after-init

# Optional: run seed data
cat /opt/clinicflow/seed_data.py | docker exec -i odoo_clinicflow_prod \
  odoo shell -d clinicflow --no-http
```

---

## Step 5 — Configure Cloudflare Tunnel

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

## Step 6 — Post-Deploy Configuration (Manual in Odoo UI)

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

## Step 7 — Keeping the Code Updated

```bash
# On the VPS
cd /opt/clinicflow
git pull origin main

# Then upgrade all ClinicFlow modules
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
| Blank page / CSS broken after CF Tunnel | Ensure `proxy_mode = True` in `odoo.prod.conf` |
| 502 Bad Gateway | Check container is running: `docker ps` |
| Module not found | Verify `/opt/clinicflow` is mounted at `/mnt/extra-addons` |
| ARM64 image pull fails | Run `docker pull --platform linux/arm64 odoo:19.0` to confirm |
| Session keeps expiring | Set `web.base.url` to the correct HTTPS domain in System Parameters |
