# A10 Corp - Sales Fulfillment Application

## Project Description
A containerized Sales Fulfillment Application designed as a study exercise to explore Azure Kubernetes Services (AKS) implementation. It serves as a front-end for service providers to streamline client onboarding, aligned with Azure's Well-Architected Framework pillars.

## Tech Stack
- **Frontend:** Python FastHTML, MonsterUI
- **Backend:** Python FastAPI
- **Database:** SQLite (Local/Persistent), Azure Cosmos DB / SQL (Planned)
- **Infrastructure:** Docker, Kubernetes (Kind/AKS), Helm, Terraform

## Developer Persona
I am an interactive CLI agent specializing in software engineering, focusing on clear, idiomatic code, strict adherence to project conventions, and safe, efficient assistance.

## Current Status
- ✅ Project scaffolding created.
- ✅ Basic FastAPI backend implemented with unit tests.
- ✅ FastHTML frontend implemented with unit tests.
- ✅ Local Kind cluster configuration and setup script created.
- ✅ Manual testing verified frontend-backend integration and UI flow.
- ✅ Migrated raw K8s manifests to Helm Chart for multi-environment support.
- ✅ Reorganized repository structure for Dev/Stage/Prod (Helm & Terraform).
- ✅ Fixed local automated tests (backend DB initialization and frontend UI text).
- ✅ Verified persistence in Kind cluster using PVCs.
- ✅ Set up Dev CI workflow (Linting, Security, Unit Tests with Coverage) via GitHub Actions.
- ✅ Defined Platform Infrastructure requirements for Azure Stage environment.

## TODO List
- [ ] **Infrastructure:** Implement AKS and Database Terraform modules in this repo.
- [ ] **Cloud Deploy:** Implement Job #2 (Stage) and Job #3 (Prod) in GitHub Actions.
- [ ] **Security:** Implement Azure AD (Entra ID) authentication for application.
- [ ] **Observability:** Set up Azure Monitor and Log Analytics integration.

## Next Session Plan
1.  **Azure Integration:**
    - Consume Platform outputs (Networking, Identities) from the landing repo.
    - Provision the AKS Cluster and Azure SQL/CosmosDB via Terraform in this repo.
2.  **CI/CD Completion:**
    - Extend GitHub Actions to build Docker images and push to ACR.
    - Implement Helm deployment to Stage AKS.
