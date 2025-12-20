from fasthtml.common import *
from monsterui.all import *
import httpx
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Using 'zinc' theme in light mode for the clean Google-style look
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

# Helper for icons
def ArrowLeftIcon(cls=""):
    return Svg(cls=cls, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewBox="0 0 24 24", fill="none", stroke="currentColor", stroke_width="2", stroke_linecap="round", stroke_linejoin="round")(
        Path(d="m12 19-7-7 7-7"),
        Path(d="M19 12H5")
    )

def CheckIcon(cls=""):
    return Svg(cls=cls, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewBox="0 0 24 24", fill="none", stroke="currentColor", stroke_width="2", stroke_linecap="round", stroke_linejoin="round")(
        Path(d="M20 6 9 17l-5-5")
    )

@rt("/")
async def index():
    return Title("A10 Corp - Sales Fulfillment"), Container(cls='mt-4 md:mt-8 max-w-5xl px-4 md:px-6')(
        Div(cls="mb-4 md:mb-6 flex justify-end")(
            H1("A10 Corp", cls="bg-sky-50 text-sky-900 px-6 py-3 rounded-xl shadow-md inline-block border border-sky-100 text-xl md:text-2xl font-semibold tracking-wide"),
        ),
        Div(cls="flex items-center gap-4 mb-4 md:mb-6")(
            A(href="#")(
                ArrowLeftIcon(cls="text-zinc-600 hover:text-zinc-900 w-5 h-5 md:w-6 md:h-6")
            ),
            H2("Client Onboarding", cls="text-2xl md:text-3xl font-normal text-zinc-800")
        ),
        Card(cls="p-6 md:p-8 shadow-sm border-zinc-200 bg-white rounded-2xl")(
            Div(cls="mb-6 md:mb-8")(
                H3("Keep track of your submissions", cls="text-lg md:text-xl font-medium text-zinc-900"),
                P("Provide company information to initiate the service agreement.", cls="text-zinc-500 text-sm md:text-base mt-1"),
            ),
            id="onboarding-container"
        )(
            basic_info_form()
        )
    )

def basic_info_form():
    input_cls = "bg-white border-zinc-200 h-10 focus:ring-zinc-200 focus:border-zinc-400 rounded-lg w-full"
    label_cls = "text-sm font-medium text-zinc-700 mb-1 block"
    
    return Form(hx_post="/engagement-info", hx_target="#onboarding-container", hx_swap="innerHTML")(
        Grid(cols=1, gap=4)(
            Div(cls="border-b border-zinc-100 pb-2 mb-2")(
                P("Company Details", cls="text-base font-semibold text-zinc-900")
            ),
            Div(cls="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6")(
                Div(P("Company Name", cls=label_cls), Input(name="company_name", placeholder="e.g. Acme Corp", required=True, cls=input_cls)),
                Div(P("Industry", cls=label_cls), Input(name="industry", placeholder="e.g. Technology", required=True, cls=input_cls)),
            ),
            Div(cls="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6")(
                Div(P("Contact Name", cls=label_cls), Input(name="contact_name", placeholder="Full Name", required=True, cls=input_cls)),
                Div(P("Contact Email", cls=label_cls), Input(name="contact_email", type="email", placeholder="email@example.com", required=True, cls=input_cls)),
            ),
            Div(cls="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6")(
                Div(P("Contact Phone", cls=label_cls), Input(name="contact_phone", placeholder="+1...", required=True, cls=input_cls)),
                Div(P("Company Size", cls=label_cls), Input(name="company_size", type="number", placeholder="100", required=True, cls=input_cls)),
            ),
            Div(P("Company Address", cls=label_cls), TextArea(name="address", placeholder="Full street address", required=True, rows=3, cls="bg-white border-zinc-200 focus:ring-zinc-200 focus:border-zinc-400 rounded-lg p-2 w-full")),
        ),
        
        Div(cls="flex justify-end mt-6 md:mt-8 pt-4 md:pt-6 border-t border-zinc-100")(
            Button("Next step", type="submit", cls=ButtonT.primary + " h-10 px-8 rounded-full text-sm font-medium")
        )
    )

@rt("/engagement-info")
async def post_engagement_info(request: Request):
    form_data = await request.form()
    hidden_fields = [Input(type="hidden", name=k, value=v) for k, v in form_data.items()]
    
    input_cls = "bg-white border-zinc-200 h-10 md:h-12 focus:ring-zinc-200 focus:border-zinc-400 rounded-lg w-full"
    label_cls = "text-sm font-medium text-zinc-700 mb-2 block"

    return Div(
        Div(cls="mb-8 md:mb-10")(
            H3("Engagement details", cls="text-lg md:text-xl font-medium text-zinc-900"),
            P("Define the scope and budget for this project.", cls="text-zinc-500 text-sm md:text-base mt-2"),
        ),
        Form(hx_post="/submit-onboarding", hx_target="#onboarding-container", hx_swap="innerHTML")(
            *hidden_fields,
            Grid(cols=1, gap=6)(
                Div(cls="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10")(
                    Div(P("Service Type", cls=label_cls),
                        Select(
                            Option("Select a service", disabled=True, selected=True, value=""),
                            Option("DevOps Consulting", value="devops"),
                            Option("Cloud Migration", value="migration"),
                            Option("Site Reliability Engineering", value="sre"),
                            Option("Custom Development", value="custom"),
                            name="service_type", required=True, cls=input_cls
                        )
                    ),
                    Div(P("Budget Range", cls=label_cls), Input(name="budget_range", placeholder="e.g. $50k - $100k", required=True, cls=input_cls)),
                ),
                Div(cls="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10")(
                    Div(P("Project Scope", cls=label_cls), Input(name="project_scope", placeholder="Short summary", required=True, cls=input_cls)),
                    Div(P("Timeline", cls=label_cls), Input(name="timeline", placeholder="e.g. 3 months", required=True, cls=input_cls)),
                ),
                Div(P("Additional Notes", cls=label_cls), TextArea(name="notes", placeholder="Any specific requirements...", rows=5, cls="bg-white border-zinc-200 focus:ring-zinc-200 focus:border-zinc-400 rounded-lg p-3 w-full")),
            ),
            
            Div(cls="flex flex-col-reverse md:flex-row justify-between mt-8 md:mt-12 pt-6 md:pt-8 border-t border-zinc-100 gap-4 md:gap-0")(
                Button("Back", hx_get="/", hx_target="#onboarding-container", hx_swap="innerHTML", cls="text-zinc-500 hover:text-zinc-900 font-medium px-4 h-10 md:h-12 flex items-center justify-center"),
                Button("Complete Submission", type="submit", cls=ButtonT.primary + " h-10 md:h-12 px-8 md:px-10 rounded-full text-sm md:text-base font-medium w-full md:w-auto")
            )
        )
    )

@rt("/submit-onboarding")
async def submit(request: Request):
    form_data = await request.form()
    
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
        
        return Div(cls="text-center py-12")(
            Div(cls="bg-green-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6")(
                CheckIcon(cls="text-green-600 text-3xl")
            ),
            H2("Submission Successful", cls="text-2xl font-medium text-zinc-900"),
            P("We've received your onboarding request and created a reference ID.", cls="text-zinc-500 mt-2"),
            
            Div(cls="mt-10 mb-10 p-6 bg-zinc-50 border border-zinc-100 rounded-xl inline-block min-w-[280px]")(
                P("Reference ID", cls="text-xs uppercase tracking-[0.1em] font-bold text-zinc-400 mb-2"),
                P(client_id, cls="text-2xl font-mono font-medium text-zinc-800 tracking-tight")
            ),
            
            Div(cls="pt-6 border-t border-zinc-100")(
                A("Return to home", href="/", cls="text-zinc-600 hover:text-zinc-900 font-medium")
            )
        )
    except Exception as e:
        return Div(cls="bg-red-50 text-red-700 p-6 rounded-xl border border-red-100")(
            H3("Submission failed", cls="font-bold"),
            P(str(e), cls="text-sm mt-2")
        )

if __name__ == "__main__":
    serve(port=5003)
