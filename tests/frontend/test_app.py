from fasthtml.common import *
from src.frontend.app import app
from starlette.testclient import TestClient

client = TestClient(app)

def test_index():
    print("\n[TEST] Fetching index page...")
    response = client.get("/")
    print(f"[TEST] Index page status: {response.status_code}")
    assert response.status_code == 200
    assert "A10 Corp - Sales Fulfillment" in response.text
    assert "Client Onboarding" in response.text

def test_engagement_info_step():
    print("\n[TEST] Submitting basic info form...")
    # Simulate first step submission
    data = {
        "company_name": "Test Corp",
        "industry": "Tech",
        "contact_name": "John Doe",
        "contact_email": "john@example.com",
        "contact_phone": "1234567890",
        "company_size": "100",
        "address": "123 Test St"
    }
    response = client.post("/engagement-info", data=data)
    print(f"[TEST] Engagement form load status: {response.status_code}")
    
    assert response.status_code == 200
    assert "Engagement details" in response.text
    # Verify hidden fields are present
    assert 'name="company_name" value="Test Corp"' in response.text
