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
- ✅ Added E2E Integration Tests (Kind + Playwright) to CI pipeline.
- ✅ Implemented AKS Terraform Module (Stage and Dev environments configured).
- ✅ Set up GitHub OIDC for keyless Azure authentication.
- ✅ Implemented **Dev On-Demand** workflow for manual cloud lab testing.
- ✅ Defined Platform Infrastructure requirements for Azure Stage environment.
- ✅ Fixed and codified AKS-to-ACR permissions and NSG routing rules.
- ✅ Implemented Azure SQL Terraform module and integrated it into Dev environment.
- ✅ Updated backend application with MSSQL drivers and conditional database logic.
- ✅ Improved **Dev On-Demand** workflow with automatic SQL provisioning and full teardown.
- ✅ Fixed FastHTML infinite refresh loop by making live reload configurable.

## TODO List
- [x] **Infrastructure:** Implement Database Terraform module in this repo.
- [ ] **Infrastructure:** Refactor VNET/Subnet/NSG ownership from Foundation to this repo (Workload Landing Zone).
- [ ] **Cloud Deploy:** Implement Job #2 (Stage) and Job #3 (Prod) in GitHub Actions.
- [ ] **Security:** Implement Azure AD (Entra ID) authentication for application.
- [ ] **Observability:** Set up Azure Monitor and Log Analytics integration.

## Next Session Plan
1.  **DevOps Pipeline Overhaul:**
    - Update `sales_fulfillment-devops.yml` to include `terraform plan` in the validation phase.
    - Implement the Stage deployment job with a manual approval gate.
    - Implement a Blue/Green strategy for Production (Green deploy -> Approval -> Switch).
2.  **Resource Management:**
    - Create `teardown-on-demand.yml` for manual, environment-specific cleanup.
3.  **Security Implementation:**
    - Implement Azure AD (Entra ID) authentication for the frontend.
