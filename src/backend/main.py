from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, String
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import os
import uuid

# --- Database Setup ---
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/sales_fulfillment.db")

# check_same_thread=False is only needed (and valid) for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

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
    client_id: str = Field(sa_type=String(50), index=True, unique=True)
    
    # Key Business Fields (Promoted for Indexing/Querying)
    company_name: str = Field(sa_type=String(255), index=True)
    industry: str = Field(sa_type=String(100), index=True)
    service_type: str = Field(sa_type=String(100), index=True)
    
    # Full Payload (JSON Storage for Flexibility)
    payload: str = Field(sa_type=String) # VARCHAR(MAX) equivalent

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