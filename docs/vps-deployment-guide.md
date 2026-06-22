# ClinicFlow — VPS Deployment Guide (Shared Cloudflare Tunnel & Network)

**Target**: Oracle A1Flex (ARM64) · Docker · Portainer · Cloudflare Tunnel  
**Domain**: `demoerp.clinicflow.vet`  
**Odoo**: 19.0 CE · PostgreSQL 15

This deployment guide uses **Portainer Stacks** with Git integration to achieve a **zero-SSH / zero-terminal** deployment process. It is configured to reuse the existing Cloudflare Tunnel and network (`clinicflow-sam_clinic-network`) from your existing `clinicflow-sam` stack, saving VPS resources and consolidating entry points.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Oracle A1Flex VPS | Ubuntu 22.04 recommended (with Portainer CE running) |
| Portainer CE | Running and accessible on the VPS |
| Existing Stack | The `clinicflow-sam` stack must be running on the VPS, which provides the private network `clinicflow-sam_clinic-network` and the `clinic-flow-tunnel` Cloudflare Tunnel. |
| DNS / Cloudflare | Control of `demoerp.clinicflow.vet` in the Cloudflare Dashboard |
| Git Repo Access | Portainer needs to read this repository (can be made public during deployment or accessed using a GitHub Personal Access Token) |

> **ARM64 Note**: `odoo:19.0` on Docker Hub publishes a multi-arch manifest including `linux/arm64`. No custom image compilation is needed.

---

## Step 1 — Deploy the Stack in Portainer

Portainer will clone this repository directly and deploy Odoo and PostgreSQL as a new stack connected to the existing `clinicflow-sam_clinic-network` network.

1. Log into your **Portainer Dashboard**.
2. Navigate to **Stacks** → **Add stack**.
3. Set the stack **Name** (e.g., `clinicflow-odoo`).
4. Under **Build method**, select **Repository**.
5. Fill in the **Repository details**:
   - **Repository URL**: `https://github.com/YOUR_ORG/clinicflow-on-odoo.git` (replace with your repository URL).
   - **Repository reference**: `refs/heads/main`
   - **Compose path**: `docker-compose.prod.yml`
6. **Authentication** (if the repository is private):
   - Toggle **Authentication** ON.
   - Enter your **GitHub Username** and a **Personal Access Token (PAT)** as the password.
7. **Environment variables**:
   Under the environment variables section, click **Advanced mode** and paste the following (replacing with your secure values):
   ```env
   DB_PASSWORD=YOUR_STRONG_DATABASE_PASSWORD
   MASTER_PASSWORD=YOUR_ODOO_ADMIN_MASTER_PASSWORD
   ```
   *(Note: No Cloudflare Tunnel token is needed here because we are using your existing running tunnel container).*
8. Click **Deploy the stack**.

---

## Step 2 — Database Initialization & Seeding (Automated)

Once you deploy the stack, the deployment and setup happen automatically:

1. **PostgreSQL** starts up and becomes healthy.
2. The **`odoo_init`** container starts. It runs the [init_odoo.py](file:///d:/MyApps/For%20SAM/clinicflow-on-odoo/config/init_odoo.py) script which:
   - Waits for Postgres to be fully ready.
   - Checks if Odoo database tables already exist.
   - Since it's a new database, it runs Odoo to install all custom modules: `clinicflow_core`, `clinicflow_patient`, `clinicflow_clinical`, `clinicflow_billing`, `clinicflow_ai`, `clinicflow_outreach`.
   - Runs [seed_data.py](file:///d:/MyApps/For%20SAM/clinicflow-on-odoo/seed_data.py) automatically inside the Odoo shell.
3. Once initialization is finished, the `odoo_init` container exits successfully (`exit code 0`).
4. The main **`odoo`** web server container starts up automatically (because it depends on `odoo_init` completing successfully) and connects to `clinicflow-sam_clinic-network`.

> **Tip**: You can view the setup logs by clicking on the `odoo_clinicflow_init` container in Portainer and checking its logs.

---

## Step 3 — Route Traffic via Existing Cloudflare Tunnel

Because the new Odoo stack joins the same Docker network (`clinicflow-sam_clinic-network`) as your existing Cloudflare Tunnel container (`clinic-flow-tunnel`), you only need to add a routing rule in Cloudflare Zero Trust:

1. Go to your **Cloudflare Zero Trust Dashboard** → **Networks** → **Tunnels**.
2. Click on the running tunnel that corresponds to your `clinicflow-sam` stack (e.g., `ClinicFlow-Production`).
3. Select **Configure** and go to the **Public Hostnames** tab.
4. Click **Add a public hostname**.
5. Fill in the details:
   - **Subdomain**: `demoerp`
   - **Domain**: `clinicflow.vet` (or your registered domain)
   - **Type**: `HTTP`
   - **URL**: `odoo_clinicflow_prod:8069`
6. Click **Save hostname**.

*Cloudflare Tunnel will now securely route all traffic destined for `https://demoerp.clinicflow.vet` directly to the `odoo_clinicflow_prod` container via the internal Docker network.*

---

## Step 4 — Post-Deploy Configuration (Manual in Odoo UI)

After the containers are running, navigate to `https://demoerp.clinicflow.vet` in your browser:

1. **Log in to Odoo** using the default administrator credentials (typically `admin` / `admin`, or as defined in the seed data).
2. **Set `web.base.url`**  
   Go to **Settings** → **Technical** → **Parameters** → **System Parameters**.  
   Find `web.base.url` and set its value to `https://demoerp.clinicflow.vet`.
3. **Configure Company details**  
   Go to **Settings** → **Companies** → **New** to configure name, currency, timezone, and address.
4. **Change Administrator password**  
   Go to **Settings** → **Users** → **Administrator** → **Change Password** to set a secure password.

---

## Step 5 — Keeping the Code Updated (Redeploying)

Whenever you push new changes to GitHub, you can pull the latest changes and upgrade modules directly from Portainer:

1. In Portainer, go to **Stacks** and select your Odoo stack.
2. Click **Editor**.
3. Click the **Pull and redeploy** button.
4. This instructs Portainer to:
   - Pull the latest code from GitHub.
   - Re-run the **`odoo_init`** service, which will detect that the database is already initialized and automatically run the Odoo module upgrade command (`-u`) to apply any module updates.
   - Start the main **`odoo`** web container with the updated code.

---

## Backup

Since Portainer automatically pulls and clones the stack's files locally on the host under `/data/compose/<stack_id>/`, you can schedule these backups on the VPS host:

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

## Troubleshooting

| Problem | Fix |
|---|---|
| Blank page / CSS broken after Cloudflare Tunnel | Ensure `proxy_mode = True` is passed via `ODOO_PROXY_MODE=True` in environment variables. |
| 502 Bad Gateway | Check if `odoo_clinicflow_prod` is running. If not, check if `odoo_clinicflow_init` has finished with exit code 0. Also verify that the tunnel hostname is routed to `odoo_clinicflow_prod:8069` exactly. |
| Modules not showing up | Ensure `ODOO_ADDONS_PATH` includes `/mnt/extra-addons` and that the git repository has been cloned successfully by Portainer. |
| DB connection timed out | Verify that the `DB_PASSWORD` matches between PostgreSQL and Odoo environment variables. |
| Odoo session keeps expiring | Ensure you have correctly configured the `web.base.url` System Parameter to `https://demoerp.clinicflow.vet`. |
