from fastapi.testclient import TestClient
import os

# Use a local file for testing to avoid connection isolation issues with :memory:
TEST_DB = "test_run.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from src.backend.main import app, create_db_and_tables

# Explicitly create tables for the test environment
create_db_and_tables()

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_submit_onboarding():
    payload = {
        "basic_info": {
            "company_name": "Test Corp",
            "address": "123 Test St",
            "industry": "Tech",
            "contact_name": "John Doe",
            "contact_email": "john@example.com",
            "contact_phone": "1234567890",
            "company_size": 100
        },
        "engagement_info": {
            "service_type": "devops",
            "project_scope": "Test Scope",
            "timeline": "3 months",
            "budget_range": "$50k",
            "notes": "No notes"
        }
    }
    response = client.post("/submit", json=payload)
    if response.status_code != 200:
        print(f"Error Response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "client_id" in data
    assert data["client_id"].startswith("CL-")

# Cleanup after tests
def teardown_module(module):
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass # Sometimes file is locked on Windows/WSL
