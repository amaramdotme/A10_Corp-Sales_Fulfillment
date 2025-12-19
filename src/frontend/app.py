from fasthtml.common import *
from monsterui.all import *
import httpx
import os
import uuid

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Using 'zinc' theme for a neutral, professional look similar to the screenshot
hdrs = Theme.zinc.headers(mode='light')
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
    return Title("A10 Corp - Sales Fulfillment"), Container(cls='mt-10 max-w-3xl')(
        Card(
            H3("Client Onboarding"),
            P("Please fill out the company details to get started.", cls="text-muted text-sm mb-6"),
            id="onboarding-container"
        )(
            basic_info_form()
        )
    )

def basic_info_form():
    return Form(hx_post="/engagement-info", hx_target="#onboarding-container", hx_swap="innerHTML")(
        Grid(cols=2, gap=4)(
            Label("Company Name", Input(name="company_name", placeholder="Acme Corp", required=True)),
            Label("Industry", Input(name="industry", placeholder="Technology", required=True)),
        ),
        Grid(cols=2, gap=4, cls="mt-4")(
            Label("Contact Name", Input(name="contact_name", placeholder="John Doe", required=True)),
            Label("Contact Email", Input(name="contact_email", type="email", placeholder="john@example.com", required=True)),
        ),
        Grid(cols=2, gap=4, cls="mt-4")(
            Label("Contact Phone", Input(name="contact_phone", placeholder="+1 (555) 000-0000", required=True)),
            Label("Company Size", Input(name="company_size", type="number", placeholder="100", required=True)),
        ),
        Label("Company Address", TextArea(name="address", placeholder="1234 Market St, San Francisco, CA", required=True), cls="mt-4"),
        
        Div(cls="flex justify-end mt-6")(
            Button("Next: Engagement Details", type="submit", cls=ButtonT.primary)
        )
    )

@rt("/engagement-info")
async def post_engagement_info(request: Request):
    # Store basic info in hidden inputs for the next step
    form_data = await request.form()
    
    # Hidden fields to carry over Phase 1 data
    hidden_fields = [Input(type="hidden", name=k, value=v) for k, v in form_data.items()]
    
    return Div(
        H3("Engagement Details"),
        P("Tell us about your project needs.", cls="text-muted text-sm mb-6"),
        Form(hx_post="/submit-onboarding", hx_target="#onboarding-container", hx_swap="innerHTML")(
            *hidden_fields,
            Grid(cols=2, gap=4)(
                Label("Service Type",
                    Select(
                        Option("Select an option", disabled=True, selected=True, value=""),
                        Option("DevOps Consulting", value="devops"),
                        Option("Cloud Migration", value="migration"),
                        Option("Site Reliability Engineering", value="sre"),
                        Option("Custom Development", value="custom"),
                        name="service_type", 
                        required=True,
                        cls="w-full" 
                    )
                ),
                Label("Budget Range", Input(name="budget_range", placeholder="$50k - $100k", required=True)),
            ),
            Grid(cols=2, gap=4, cls="mt-4")(
                Label("Project Scope", Input(name="project_scope", placeholder="Migration to Azure", required=True)),
                Label("Timeline", Input(name="timeline", placeholder="3 months", required=True)),
            ),
            Label("Additional Notes", TextArea(name="notes", placeholder="Any specific requirements..."), cls="mt-4"),
            
            Div(cls="flex justify-between mt-6")(
                Button("Back", hx_get="/", hx_target="#onboarding-container", hx_swap="innerHTML", cls=ButtonT.secondary),
                Button("Complete Submission", type="submit", cls=ButtonT.primary)
            )
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
            Div("✅", cls="text-6xl text-green-500 mb-4"),
            H2("Submission Received!", cls="text-2xl font-bold"),
            P("We have safely recorded your onboarding request.", cls="text-muted mt-2"),
            
            Div(cls="mt-6 bg-zinc-100 p-4 rounded border border-zinc-200 inline-block")(
                P("Reference ID", cls="text-xs uppercase tracking-wider text-zinc-500"),
                P(client_id, cls="text-xl font-mono font-bold text-zinc-800")
            ),
            
            Div(cls="mt-8")(
                A("Submit Another", href="/", cls=ButtonT.primary)
            )
        )
    except Exception as e:
        return Div(cls="bg-red-50 text-red-700 p-4 rounded border border-red-200")(
            H3("Error Submitting Form", cls="font-bold"),
            P(str(e), cls="text-sm mt-1")
        )

if __name__ == "__main__":
    serve(port=5003)
