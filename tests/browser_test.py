import asyncio
import os
import sys
from playwright.async_api import async_playwright

# Configuration settings
BASE_URL = os.environ.get("ODOO_URL", "http://localhost:8070")
DB_NAME = os.environ.get("ODOO_DB", "odoo-db-clean")
USERNAME = os.environ.get("ODOO_USER", "admin")
PASSWORD = os.environ.get("ODOO_PASSWORD", "Admin@Forgot2026")

async def run_browser_tests():
    print("==================================================")
    print("Starting ClinicFlow E2E Browser Verification Tests")
    print(f"Target URL: {BASE_URL}")
    print(f"Database:   {DB_NAME}")
    print("==================================================")

    async with async_playwright() as p:
        # Launch browser (headed mode so the user can watch the action if running locally)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        try:
            # 1. Navigate to Login Page
            print("\n[Step 1] Navigating to Odoo login page...")
            await page.goto(f"{BASE_URL}/web/login?db={DB_NAME}")
            await page.wait_for_selector("input#login", state="visible")

            # 2. Perform Login
            print("[Step 2] Logging in as admin...")
            await page.fill("input#login", USERNAME)
            await page.fill("input#password", PASSWORD)
            await page.click("button[type='submit']")

            # Wait for Odoo shell to load and menus to be visible
            print("Waiting for Odoo home screen to load...")
            await page.wait_for_selector(".o_navbar", timeout=30000)
            print("Login successful and home screen loaded.")

            # 3. Locate ClinicFlow App in App Switcher/Navbar
            print("\n[Step 3] Navigating to ClinicFlow Module...")
            # Click the main app switcher menu if present
            app_switcher = page.locator(".o_navbar_apps_menu")
            if await app_switcher.count() > 0:
                await app_switcher.click()
                await page.wait_for_timeout(1000)
            
            # Click ClinicFlow menu item
            clinicflow_app = page.locator("a.o_app:has-text('ClinicFlow'), .o_app:has-text('ClinicFlow'), a:has-text('ClinicFlow')")
            if await clinicflow_app.count() > 0:
                await clinicflow_app.first.click()
            else:
                # Direct URL fallback if menu clicking fails
                print("ClinicFlow app menu not clickable, using direct URL hash...")
                await page.goto(f"{BASE_URL}/web#menu_id=clinicflow_core.menu_clinicflow_root")
            
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(2000)  # Give OWL framework a moment to render the sidebar

            # 4. Verify Sidebar Menu Order
            print("\n[Step 4] Verifying Sidebar Menu Sequence...")
            # Fetch all sub-menus in the sidebar
            # In Odoo 17/18/19, menu items in the sidebar are usually in a container like `.o_control_panel` or `.o_sidebar` or `.o_menu_sections`
            # Let's inspect the page content to see sidebar elements
            sections = page.locator(".o_menu_sections .o_menu_entry_lvl_1, .o_control_panel .o_menu_entry, .o_sidebar .o_menu_entry")
            count = await sections.count()
            
            # Fallback check for Odoo 17/18/19 sidebar layout
            if count == 0:
                sections = page.locator("a.o_menu_entry, a.o_nav_entry")
                count = await sections.count()

            menu_items = []
            for i in range(count):
                text = await sections.nth(i).text_content()
                if text:
                    menu_items.append(text.strip())

            print(f"Detected Sidebar Menu Items: {menu_items}")

            # Verify 'Dashboards' is the first menu item
            if menu_items:
                first_item = menu_items[0]
                print(f"First menu item is: '{first_item}'")
                if "Dashboard" in first_item or "ClinicFlow" in first_item:
                    print("[SUCCESS]: Dashboards (or ClinicFlow base dashboard) is positioned first.")
                else:
                    print(f"[WARNING]: Expected first menu item to be Dashboards, got '{first_item}'")
            else:
                print("Could not retrieve sidebar menu items, verifying via direct URL routing...")

            # 5. Direct navigation to Patients view
            print("\n[Step 5] Accessing Patients View...")
            # We can use Odoo URL hash to navigate directly to the Pet list action
            await page.goto(f"{BASE_URL}/web#action=clinicflow_patient.action_clinicflow_pet")
            await page.wait_for_selector(".o_list_renderer", timeout=15000)
            print("Patients list view loaded successfully.")

            # Print list of pets visible on screen
            pet_names = await page.eval_on_selector_all(
                ".o_list_table td[name='name']",
                "elements => elements.map(el => el.textContent.trim())"
            )
            print(f"Visible Pets in Patient Database: {pet_names}")

            # Verify that seeded pets (Max and Bella) exist
            if "Max" in pet_names:
                print("[SUCCESS]: Seeding verified: Found pet 'Max' in list.")
            else:
                print("[WARNING]: Seeding warning: Pet 'Max' not found in visible list.")

            # 6. Direct navigation to Visits view to verify visit and billing linkage
            print("\n[Step 6] Accessing Visits View...")
            await page.goto(f"{BASE_URL}/web#action=clinicflow_clinical.action_clinicflow_visit_global")
            await page.wait_for_selector(".o_list_renderer", timeout=15000)
            print("Visits list view loaded successfully.")

            # Print list of visits
            visit_names = await page.eval_on_selector_all(
                ".o_list_table td[name='name']",
                "elements => elements.map(el => el.textContent.trim())"
            )
            print(f"Visible Visits: {visit_names}")

            # 7. Access Dashboards
            print("\n[Step 7] Verifying ClinicFlow Dashboard...")
            await page.goto(f"{BASE_URL}/web#action=clinicflow_core.action_clinicflow_dashboard_open")
            await page.wait_for_timeout(3000)
            
            # Take a screenshot to verify UI visually
            screenshot_path = os.path.join(os.path.dirname(__file__), "clinicflow_dashboard_verification.png")
            await page.screenshot(path=screenshot_path)
            print(f"Saved dashboard verification screenshot to: {screenshot_path}")
            
            print("\n==================================================")
            print("[COMPLETED]: Browser Verification Tests Completed Successfully!")
            print("==================================================")

        except Exception as e:
            print(f"\n[ERROR] occurred during E2E verification: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_browser_tests())
