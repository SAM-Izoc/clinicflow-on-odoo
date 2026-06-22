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

env = os.environ.copy()

if db_initialized:
    print("Database is already initialized. Upgrading modules...")
    cmd = [
        "odoo",
        "-d", db_name,
        "-u", modules,
        "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons",
        "--db_host=" + db_host,
        "--db_port=5432",
        "--db_user=" + db_user,
        "--db_password=" + db_password,
        "--stop-after-init"
    ]
else:
    print("Database is new. Installing ClinicFlow modules...")
    cmd = [
        "odoo",
        "-d", db_name,
        "-i", modules,
        "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons",
        "--db_host=" + db_host,
        "--db_port=5432",
        "--db_user=" + db_user,
        "--db_password=" + db_password,
        "--stop-after-init"
    ]

print(f"Running command: {' '.join(cmd)}")
result = subprocess.run(cmd, env=env, capture_output=True, text=True)
print("STDOUT:")
print(result.stdout)
print("STDERR:")
print(result.stderr)

if result.returncode != 0:
    print(f"Odoo command failed with return code {result.returncode}")
    sys.exit(result.returncode)

if not db_initialized:
    print("Loading seed data...")
    seed_file = "/mnt/extra-addons/seed_data.py"
    if os.path.exists(seed_file):
        try:
            with open(seed_file, "r", encoding="utf-8") as f:
                seed_code = f.read()
            
            cmd_shell = [
                "odoo",
                "shell",
                "-d", db_name,
                "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons",
                "--db_host=" + db_host,
                "--db_port=5432",
                "--db_user=" + db_user,
                "--db_password=" + db_password,
                "--no-http"
            ]
            print(f"Running shell command: {' '.join(cmd_shell)}")
            result_shell = subprocess.run(cmd_shell, input=seed_code, text=True, env=env, capture_output=True)
            print("SHELL STDOUT:")
            print(result_shell.stdout)
            print("SHELL STDERR:")
            print(result_shell.stderr)
            
            if result_shell.returncode != 0:
                print(f"Seed data execution failed with return code {result_shell.returncode}")
                sys.exit(result_shell.returncode)
            print("Seed data loaded successfully.")
        except Exception as e:
            print(f"Failed to load seed data: {e}")
            sys.exit(1)
    else:
        print(f"WARNING: Seed data script not found at {seed_file}")

print("=== ClinicFlow Database Setup/Upgrade Complete ===")
sys.exit(0)
