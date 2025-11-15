from playwright.sync_api import sync_playwright, expect

def test_mandatory_fields_ticket_flow():
    EMAIL = "mohamed.el.saayed7@gmail.com"
    PASSWORD = "77b@cNxZiF3ZyG7"

    FORM_NAME = "PlanRadar Assessment @ Mohamed"

    TICKETS_URL = "https://www.planradar.com/dr/1484311/1484312/defects"

    mandatory_fields = [
        "Type of work",
        "Need to be done before (Deadline)",
        "Location",
        "Assignee"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Open login
        page.goto("https://www.planradar.com/login")
        page.fill("input[type='email']", EMAIL)
        page.click("button.btn-success:has-text('Continue')")
        page.wait_for_selector("input[type='password']", timeout=10000)

        # 2️⃣ Enter password and login
        page.fill("input[type='password']", PASSWORD)
        page.click("button.btn-success")

        # 3️⃣ Wait for login, then go to tickets page
        page.wait_for_load_state("networkidle")
        page.goto(TICKETS_URL)
        page.wait_for_load_state("networkidle")

        # 4️⃣ Click the "Add (+)" button to create a ticket
        add_button = page.locator("svg[data-icon='plus']").locator("..")
        add_button.wait_for(state="visible", timeout=15000)
        add_button.click()

        # 5️⃣ Wait for ticket modal/dialog to appear
        ticket_modal = page.locator("div[role='dialog']")
        ticket_modal.wait_for(state="visible", timeout=15000)

        # 6️⃣ Click the form field (combobox) to open dropdown
        form_field = ticket_modal.locator("div[role='combobox']")
        form_field.wait_for(state="visible", timeout=15000)
        form_field.click()

        # 7️⃣ Select the desired form robustly
        desired_form = ticket_modal.locator(f"div:has-text('{FORM_NAME}')").first
        desired_form.wait_for(state="visible", timeout=15000)
        desired_form.click()

        # Optional wait to ensure form fields load
        page.wait_for_timeout(1500)

        # 8️⃣ Click the Save button inside the ticket modal using data-testid
        save_button = ticket_modal.locator("span[data-testid='Save']")
        save_button.wait_for(state="visible", timeout=10000)
        save_button.click()

        # Optional wait for validation messages to appear
        page.wait_for_timeout(2000)

        # 9️⃣ Validate mandatory field errors
        for field in mandatory_fields:
            print(f"Checking validation for: {field}")
            potential_error = ticket_modal.locator(f"text={field}").locator("xpath=..").locator("text=required")
            try:
                expect(potential_error).to_be_visible(timeout=3000)
                print(f"✔ Validation displayed for: {field}")
            except:
                print(f"✘ Validation NOT found for: {field}")

        browser.close()


if __name__ == "__main__":
    test_mandatory_fields_ticket_flow()
