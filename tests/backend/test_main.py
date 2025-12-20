from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from src.backend.main import app, get_session
import os
import tempfile

# 1. Create a temporary file for the database
test_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
test_db_path = test_db_file.name
test_db_file.close()

# 2. Create a specific engine for this test session
sqlite_url = f"sqlite:///{test_db_path}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# 3. Create tables in this temporary database
SQLModel.metadata.create_all(engine)

# 4. Define a dependency override
def get_session_override():
    with Session(engine) as session:
        yield session

# 5. Apply the override to the app
app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

def teardown_module(module):
    # Cleanup: remove the temporary file
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_health_check():
    print("\n[TEST] Running health check...")
    response = client.get("/health")
    print(f"[TEST] Health check response: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_submit_onboarding():
    print("\n[TEST] Testing client onboarding submission...")
    payload = {
        "basic_info": {
            "company_name": "Test Corp",
            "address": "123 Test St",
            "industry": "Testing",
            "contact_name": "Tester",
            "contact_email": "test@example.com",
            "contact_phone": "555-1234",
            "company_size": 50
        },
        "engagement_info": {
            "service_type": "devops",
            "project_scope": "Full automation",
            "timeline": "3 months",
            "budget_range": "$50k-$100k"
        }
    }
    
    response = client.post("/submit", json=payload)
    data = response.json()
    print(f"[TEST] Submission response: {response.status_code} - {data}")
    
    assert response.status_code == 200
    assert "client_id" in data
    assert data["message"] == "Submission received successfully"
