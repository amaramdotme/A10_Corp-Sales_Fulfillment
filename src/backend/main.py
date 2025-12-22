from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, String
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import os
import uuid
import json

# Azure Storage Imports
try:
    from azure.storage.blob import BlobServiceClient
    from azure.identity import DefaultAzureCredential
    HAS_AZURE = True
except ImportError:
    HAS_AZURE = False

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/sales_fulfillment.db")
STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")
STORAGE_CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER_NAME")

# --- Database Setup ---
# check_same_thread=False is only needed (and valid) for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- Models ---

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

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: str = Field(sa_type=String(50), index=True, unique=True)
    company_name: str = Field(sa_type=String(255), index=True)
    industry: str = Field(sa_type=String(100), index=True)
    service_type: str = Field(sa_type=String(100), index=True)
    payload: str = Field(sa_type=String) # VARCHAR(MAX) equivalent

# --- Helpers ---

async def backup_to_blob(client_id: str, data: dict):
    """Backs up the submission to Azure Blob Storage if configured."""
    if not (HAS_AZURE and STORAGE_ACCOUNT_NAME and STORAGE_CONTAINER_NAME):
        print("[BACKUP] Skipping blob backup (Azure libs or config missing)")
        return

    try:
        account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url, credential=credential)
        blob_client = blob_service_client.get_blob_client(container=STORAGE_CONTAINER_NAME, blob=f"{client_id}.json")
        
        blob_client.upload_blob(json.dumps(data, indent=2), overwrite=True)
        print(f"[BACKUP] Successfully backed up {client_id} to blob storage.")
    except Exception as e:
        # We don't want to fail the main request if backup fails, but we should log it
        print(f"[BACKUP] ERROR: Failed to backup to blob: {e}")

# --- Lifespan Events ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# --- App Definition ---
app = FastAPI(title="A10 Corp Sales Fulfillment API", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/submit")
async def submit_onboarding(submission: ClientSubmission, session: Session = Depends(get_session)):
    client_id = f"CL-{uuid.uuid4().hex[:8].upper()}"
    
    db_submission = Submission(
        client_id=client_id,
        company_name=submission.basic_info.company_name,
        industry=submission.basic_info.industry,
        service_type=submission.engagement_info.service_type,
        payload=submission.model_dump_json()
    )
    
    try:
        # 1. Save to Database
        session.add(db_submission)
        session.commit()
        session.refresh(db_submission)
        
        # 2. Backup to Blob Storage (Asynchronous/Fire-and-forget)
        await backup_to_blob(client_id, submission.model_dump())
        
        return {"client_id": client_id, "message": "Submission received successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104