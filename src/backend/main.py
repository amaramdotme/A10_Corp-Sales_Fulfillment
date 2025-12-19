from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="A10 Corp Sales Fulfillment API")

class ClientBasicInfo(BaseModel):
    company_name: str
    address: str
    industry: str
    contact_name: str
    contact_email: str
    contact_phone: str
    company_size: int

class EngagementInfo(BaseModel):
    service_type: str
    project_scope: str
    timeline: str
    budget_range: str
    notes: Optional[str] = None

class ClientSubmission(BaseModel):
    basic_info: ClientBasicInfo
    engagement_info: EngagementInfo

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/submit")
async def submit_onboarding(submission: ClientSubmission):
    # Logic to generate a unique Client ID and store data will go here
    client_id = f"CL-{uuid.uuid4().hex[:8].upper()}"
    # For now, just return the ID
    return {"client_id": client_id, "message": "Submission received successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
