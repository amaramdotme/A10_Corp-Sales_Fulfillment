# A10 Corp - Sales Fulfillment Application

This application is designed as a study exercise to explore Azure Kubernetes Services (AKS) implementation. It captures client information in two phases and generates a unique Client ID.

## Architecture

- **Frontend:** Python FastHTML with MonsterUI.
- **Backend:** FastAPI.
- **Database:** SQLite (Local) / Azure SQL (Deployed).
- **Local Dev:** Docker Compose / Kind.
- **Infrastructure:** Terraform (targeting AKS and Azure SQL).

## Getting Started

### Local Development with Docker Compose

To run the application locally using Docker Compose:

```bash
docker-compose up --build
```

- Frontend: [http://localhost:5003](http://localhost:5003)
- Backend: [http://localhost:8000](http://localhost:8000)

### Running Tests

#### Backend Tests
```bash
PYTHONPATH=. pytest tests/backend/test_main.py
```

#### Frontend Tests
```bash
PYTHONPATH=. pytest tests/frontend/test_app.py
```

## Project Structure

- `src/frontend`: FastHTML application.
- `src/backend`: FastAPI application.
- `infra/terraform`: Terraform configuration for Azure resources.
- `infra/k8s`: Kubernetes manifests and Helm charts.
- `deploy/local`: Local deployment scripts (e.g., Kind).
- `tests`: Unit and integration tests.