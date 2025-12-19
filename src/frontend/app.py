from fasthtml.common import *
from monsterui.all import *
import httpx
import os
import uuid

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

hdrs = Theme.blue.headers(mode='light')
app, rt = fast_app(hdrs=hdrs, live=True)

# Helper to call backend
async def call_backend(path, method="GET", json=None):
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{path}"
        if method == "POST":
            resp = await client.post(url, json=json)
        else:
            resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

@rt("/")
async def index():
    return Title("A10 Corp - Sales Fulfillment"), Container(cls='mt-10')(
        Card(
            H1("Client Onboarding"),
            P("Please fill out the following information to get started.", cls="text-muted"),
            id="onboarding-container"
        )(
            basic_info_form()
        )
    )

def basic_info_form():
    return Form(hx_post="/engagement-info", hx_target="#onboarding-container", hx_swap="innerHTML")(
        Grid(cols=2)(
            Input(name="company_name", placeholder="Company Name", required=True),
            Input(name="industry", placeholder="Industry", required=True),
            Input(name="contact_name", placeholder="Contact Person Name", required=True),
            Input(name="contact_email", type="email", placeholder="Contact Email", required=True),
            Input(name="contact_phone", placeholder="Contact Phone", required=True),
            Input(name="company_size", type="number", placeholder="Company Size (Employees)", required=True),
        ),
        TextArea(name="address", placeholder="Company Address", required=True, cls="mt-4"),
        Button("Next: Engagement Details", type="submit", cls="mt-4 w-full")
    )

@rt("/engagement-info")
async def post_engagement_info(request: Request):
    # Store basic info in hidden inputs for the next step
    form_data = await request.form()
    
    # Hidden fields to carry over Phase 1 data
    hidden_fields = [Input(type="hidden", name=k, value=v) for k, v in form_data.items()]
    
    return Div(
        H2("Engagement Specific Details"),
        Form(hx_post="/submit-onboarding", hx_target="#onboarding-container", hx_swap="innerHTML")(
            *hidden_fields,
            Grid(cols=1, gap=4)(
                Select(
                    Option("Select an option", disabled=True, selected=True, value=""),
                    Option("DevOps Consulting", value="devops"),
                    Option("Cloud Migration", value="migration"),
                    Option("Site Reliability Engineering", value="sre"),
                    Option("Custom Development", value="custom"),
                    label="Service Type",
                    name="service_type", 
                    required=True
                ),
                Input(name="project_scope", placeholder="Project Scope Summary", required=True),
                Input(name="timeline", placeholder="Timeline Expectations (e.g., 3 months)", required=True),
                Input(name="budget_range", placeholder="Budget Range (e.g., $50k - $100k)", required=True),
                TextArea(name="notes", placeholder="Additional Notes"),
            ),
            Button("Complete Submission", type="submit", cls="mt-4 w-full")
        )
    )

@rt("/submit-onboarding")
async def submit(request: Request):
    form_data = await request.form()
    
    # Construct the payload for backend
    payload = {
        "basic_info": {
            "company_name": form_data.get("company_name"),
            "address": form_data.get("address"),
            "industry": form_data.get("industry"),
            "contact_name": form_data.get("contact_name"),
            "contact_email": form_data.get("contact_email"),
            "contact_phone": form_data.get("contact_phone"),
            "company_size": int(form_data.get("company_size")),
        },
        "engagement_info": {
            "service_type": form_data.get("service_type"),
            "project_scope": form_data.get("project_scope"),
            "timeline": form_data.get("timeline"),
            "budget_range": form_data.get("budget_range"),
            "notes": form_data.get("notes"),
        }
    }
    
    try:
        result = await call_backend("/submit", method="POST", json=payload)
        client_id = result.get("client_id")
        
        return Div(cls="text-center p-10")(
            Div("✅", cls="text-4xl text-success mb-4"),
            H2("Submission Successful!"),
            P(f"Your unique Client ID is:", cls="mt-4"),
            H3(client_id, cls="font-mono text-2xl bg-muted p-2 rounded mt-2"),
            P("Please keep this ID for your records. Our team will contact you shortly.", cls="mt-4 text-muted"),
            A("Return Home", href="/", cls="mt-6 block text-primary underline")
        )
    except Exception as e:
        return Div(cls="bg-red-100 text-red-700 p-4 rounded")(
            H3("Error Submitting Form"),
            P(str(e))
        )

if __name__ == "__main__":
    serve(port=5003)
