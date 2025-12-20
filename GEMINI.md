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

## TODO List
- [ ] **Infrastructure:** Complete Terraform configuration for AKS, Entra ID, and Azure Monitor.
- [ ] **Cloud Deploy:** Implement CI/CD pipelines (GitHub Actions) for cloud deployment.
- [ ] **Security:** Implement Azure AD (Entra ID) authentication.
- [ ] **Observability:** Set up Azure Monitor and Log Analytics integration.

## Next Session Plan
1.  **CI/CD Strategy:**
    - Automate unit test execution.
    - Integrate security-related checks (linting, vulnerability scanning).
2.  **Terraform Poly-repo Strategy:**
    - Strategize and implement a robust Terraform structure for multi-environment management.
