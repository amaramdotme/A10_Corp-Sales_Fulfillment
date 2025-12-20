from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import os
import uuid

# --- Database Setup ---
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/sales_fulfillment.db")
# check_same_thread=False is needed for SQLite with FastAPI/multi-threading
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- Models ---

# Pydantic Schemas for API Request/Response
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

# SQLModel for Database Persistence (Hybrid: Key fields + JSON payload)
class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: str = Field(index=True, unique=True)
    
    # Key Business Fields (Promoted for Indexing/Querying)
    company_name: str = Field(index=True)
    industry: str = Field(index=True)
    service_type: str = Field(index=True)
    
    # Full Payload (JSON Storage for Flexibility)
    payload: str

# --- Lifespan Events ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    create_db_and_tables()
    yield
    # Shutdown: (Add cleanup logic here if needed)

# --- App Definition ---
app = FastAPI(title="A10 Corp Sales Fulfillment API", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/submit")
async def submit_onboarding(submission: ClientSubmission, session: Session = Depends(get_session)):
    # Generate unique Client ID
    client_id = f"CL-{uuid.uuid4().hex[:8].upper()}"
    
    # Hybrid Storage: Promote key fields, store the rest as JSON
    db_submission = Submission(
        client_id=client_id,
        company_name=submission.basic_info.company_name,
        industry=submission.basic_info.industry,
        service_type=submission.engagement_info.service_type,
        payload=submission.model_dump_json()
    )
    
    try:
        session.add(db_submission)
        session.commit()
        session.refresh(db_submission)
        return {"client_id": client_id, "message": "Submission received successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # nosec