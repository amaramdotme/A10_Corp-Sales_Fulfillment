from playwright.sync_api import Page, expect

# Define the base URL - this can be overridden by environment variables if needed
BASE_URL = "http://localhost:5003"

def test_full_onboarding_flow(page: Page):
    # 1. Navigate to the home page
    page.goto(BASE_URL)
    
    # Verify page title or header
    expect(page.locator("h2")).to_contain_text("Client Onboarding")

    # 2. Fill out Basic Info Form (Step 1)
    page.fill('input[name="company_name"]', "Test Company Inc.")
    page.fill('input[name="industry"]', "Cloud Computing")
    page.fill('input[name="contact_name"]', "John Doe")
    page.fill('input[name="contact_email"]', "john.doe@example.com")
    page.fill('input[name="contact_phone"]', "+1-555-0100")
    page.fill('input[name="company_size"]', "500")
    page.fill('textarea[name="address"]', "123 Cloud Way, Tech City")

    # Click "Next step"
    page.click('button:has-text("Next step")')

    # 3. Verify transition to Engagement Info Form (Step 2)
    # We check for a field that only exists in the second step
    expect(page.locator('select[name="service_type"]')).to_be_visible()
    expect(page.locator("h3")).to_contain_text("Engagement details")

    # 4. Fill out Engagement Info Form
    page.select_option('select[name="service_type"]', "devops")
    page.fill('input[name="budget_range"]', "$50k - $100k")
    page.fill('input[name="project_scope"]', "Full migration to Azure")
    page.fill('input[name="timeline"]', "3 months")
    page.fill('textarea[name="notes"]', "Priority on security and compliance.")

    # Click "Complete Submission"
    page.click('button:has-text("Complete Submission")')

    # 5. Verify Success Screen
    expect(page.locator("h2")).to_contain_text("Submission Successful")
    expect(page.locator("text=Reference ID")).to_be_visible()
    
    # Optional: Print the Client ID found on page for debugging logs
    # client_id = page.locator("p.font-mono").inner_text()
    # print(f"Generated Client ID: {client_id}")
