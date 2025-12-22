# A10 Corp - Sales Fulfillment Application

## Project Description
A containerized Sales Fulfillment Application designed as a study exercise to explore Azure Kubernetes Services (AKS) implementation. It serves as a front-end for service providers to streamline client onboarding, aligned with Azure's Well-Architected Framework pillars.

## Tech Stack
- **Frontend:** Python FastHTML, MonsterUI
- **Backend:** Python FastAPI
- **Database:** SQLite (Container Persistent Volumes)
- **Backup:** Azure Blob Storage (JSON backups)
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
- ✅ Added E2E Integration Tests (Kind + Playwright) to CI pipeline.
- ✅ Implemented AKS Terraform Module (Stage and Dev environments configured).
- ✅ Set up GitHub OIDC for keyless Azure authentication.
- ✅ Implemented **Dev On-Demand** workflow for manual cloud lab testing.
- ✅ Defined Platform Infrastructure requirements for Azure Stage environment.
- ✅ Fixed and codified AKS-to-ACR permissions and NSG routing rules.
- ✅ Migrated from Azure SQL to SQLite with Azure Blob Storage backups for simplicity.
- ✅ Fixed FastHTML infinite refresh loop by making live reload configurable.
- ✅ Implemented comprehensive DevOps pipeline with automated Stage deployment and Playwright verification.
- ✅ Established Blue/Green deployment strategy for Production with manual promotion.
- ✅ Created **Teardown On-Demand** workflow for safe environment decommissioning.
- ✅ Resolved `ImagePullBackOff` issues with RBAC propagation wait (60s).
- ✅ Fixed Dev On-Demand workflow (added missing Terraform Apply step).
- ✅ Configured Azure Service Endpoints for secure AKS-to-Blob Storage connectivity.
- ✅ Implemented storage account network rules to allow AKS subnet access via service endpoints.

## TODO List
- [x] **Infrastructure:** Implement Database Terraform module in this repo.
- [x] **Cloud Deploy:** Implement Job #2 (Stage) and Job #3 (Prod) in GitHub Actions.
- [ ] **Infrastructure:** Move storage account network rules to Foundation repo (currently temporary workaround).
- [ ] **Infrastructure:** Move service endpoint configuration to Foundation repo (subnet ownership).
- [ ] **Security:** Implement Azure AD (Entra ID) authentication for application.
- [ ] **Observability:** Set up Azure Monitor and Log Analytics integration.

## Next Session Plan
1.  **Infrastructure Refactoring:**
    - Move storage account network rules and service endpoint configuration to Foundation repo.
    - Better aligns with poly-repo architecture (Platform owns infrastructure, Workload consumes).
2.  **Security Implementation:**
    - Implement Azure AD (Entra ID) authentication for the frontend using MSAL or similar.
3.  **Observability:**
    - Integrate Azure Monitor and Log Analytics for better workload visibility.
