import os
import sys
import time
import subprocess
import psycopg2

print("=== Starting ClinicFlow Database Initialization/Upgrade ===")

db_host = os.environ.get("ODOO_DB_HOST", "postgres_clinicflow")
db_user = os.environ.get("ODOO_DB_USER", "odoo")
db_password = os.environ.get("ODOO_DB_PASSWORD")
db_name = "clinicflow"

# Wait for Postgres
print(f"Waiting for postgres host {db_host} to be ready...")
connected = False
for i in range(30):
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        conn.close()
        connected = True
        break
    except Exception as e:
        print(f"Postgres not ready yet ({e}). Retrying in 2 seconds...")
        time.sleep(2)

if not connected:
    print("Error: Postgres connection timed out.")
    sys.exit(1)

print("Postgres is ready. Checking database state...")

# Check if tables exist
db_initialized = False
try:
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ir_module_module');")
    db_initialized = cur.fetchone()[0]
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error checking database tables: {e}")

modules = "clinicflow_core,clinicflow_patient,clinicflow_clinical,clinicflow_billing,clinicflow_ai,clinicflow_outreach"

# Build environment for Odoo subprocess
env = os.environ.copy()

if db_initialized:
    print("Database is already initialized. Upgrading modules...")
    # Run upgrade command
    cmd = ["odoo", "-d", db_name, "-u", modules, "--stop-after-init"]
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print(f"Upgrade failed with return code {result.returncode}")
        sys.exit(result.returncode)
else:
    print("Database is new. Installing ClinicFlow modules...")
    # Run install command
    cmd = ["odoo", "-d", db_name, "-i", modules, "--stop-after-init"]
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print(f"Installation failed with return code {result.returncode}")
        sys.exit(result.returncode)
        
    print("Loading seed data...")
    seed_file = "/mnt/extra-addons/seed_data.py"
    if os.path.exists(seed_file):
        try:
            with open(seed_file, "r", encoding="utf-8") as f:
                seed_code = f.read()
            
            # Execute seed data in Odoo shell
            cmd = ["odoo", "shell", "-d", db_name, "--no-http"]
            result = subprocess.run(cmd, input=seed_code, text=True, env=env)
            if result.returncode != 0:
                print(f"Seed data execution failed with return code {result.returncode}")
                sys.exit(result.returncode)
            print("Seed data loaded successfully.")
        except Exception as e:
            print(f"Failed to load seed data: {e}")
            sys.exit(1)
    else:
        print(f"WARNING: Seed data script not found at {seed_file}")

print("=== ClinicFlow Database Setup/Upgrade Complete ===")
sys.exit(0)
