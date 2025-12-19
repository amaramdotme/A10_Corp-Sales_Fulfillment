# A10 Corp - Sales Fulfillment Application

## Project Description
A containerized Sales Fulfillment Application designed as a study exercise to explore Azure Kubernetes Services (AKS) implementation. It serves as a front-end for service providers to streamline client onboarding, aligned with Azure's Well-Architected Framework pillars.

## Tech Stack
- **Frontend:** Python FastHTML, MonsterUI
- **Backend:** Python FastAPI
- **Database:** SQLite (Local), Azure Cosmos DB / SQL (Planned)
- **Infrastructure:** Docker, Kubernetes (Kind/AKS), Terraform

## Developer Persona
I am an interactive CLI agent specializing in software engineering, focusing on clear, idiomatic code, strict adherence to project conventions, and safe, efficient assistance.

## Current Status
- ✅ Project scaffolding created.
- ✅ Basic FastAPI backend implemented with unit tests.
- ✅ FastHTML frontend implemented with unit tests.
- ✅ Dockerfiles and Docker Compose setup for local development.
- ✅ Local Kind cluster configuration and setup script created.
- ✅ Manual testing verified frontend-backend integration and UI flow.

## TODO List
- [ ] **Backend Persistence:** Implement SQLite integration in `main.py` (currently in-memory).
- [ ] **Frontend Polish:** Ensure `Select` components and other MonsterUI elements use correct headers/imports.
- [ ] **Infrastructure:** Complete Terraform configuration for AKS, Entra ID, and Azure Monitor.
- [ ] **Cloud Deploy:** Implement CI/CD pipelines (GitHub Actions) for cloud deployment.
- [ ] **Security:** Implement Azure AD (Entra ID) authentication.
- [ ] **Observability:** Set up Azure Monitor and Log Analytics integration.