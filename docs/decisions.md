# Architectural Decision Records (ADR)

This document captures key architectural decisions for the A10 Corp Sales Fulfillment Application.

## 1. Frontend Framework: FastHTML
*   **Status:** Accepted
*   **Context:** We needed a frontend framework that integrates tightly with our Python backend ecosystem and allows for rapid development of a server-rendered application.
*   **Decision:** Use **FastHTML** (with MonsterUI).
*   **Consequences:** Simplifies the stack by keeping everything in Python. Reduces the need for a separate heavy JavaScript build pipeline (like React/Angular) for this specific internal tool.

## 2. Backend Framework: FastAPI
*   **Status:** Accepted
*   **Context:** The application requires a high-performance, easy-to-use web framework for the backend API.
*   **Decision:** Use **FastAPI**.
*   **Consequences:** Provides automatic OpenAPI documentation, type safety, and high performance (async support).

## 3. Infrastructure Strategy: Poly-repo (Platform vs. Application)
*   **Status:** Accepted
*   **Context:** The organization separates "Platform" (Networking, Governance, Identity) from "Workloads" (Compute, Data).
*   **Decision:** Follow a **Poly-repo** strategy.
    *   **Platform Repo:** Manages VNETs, Resource Groups, and Governance.
    *   **Application Repo (This one):** Manages AKS clusters and Databases within the provided constraints.
*   **Consequences:** We must consume outputs (IDs, names) from the Platform repository rather than creating everything from scratch.

## 4. Azure Resource Referencing: Terraform Data Sources
*   **Status:** Accepted (2025-12-20)
*   **Context:** We need to deploy our AKS cluster into an existing Virtual Network and Resource Group managed by the Platform team. We considered reading the Platform's `tfstate` vs. querying Azure directly.
*   **Decision:** Use **Terraform Data Sources** (e.g., `data "azurerm_resource_group"`, `data "azurerm_subnet"`) to lookup resources by name.
*   **Reasoning:**
    *   Decouples our IaC from the implementation details of the Platform repo (which could change or be Bicep-based).
    *   Verifies resource existence at runtime.
    *   We have a stable list of resource names (`docs/Foundation_Resource_list.md`).
*   **Consequences:** We must ensure our input variables match the exact naming conventions used by the Platform team.

## 5. Container Orchestration: Kubernetes (AKS & Kind)
*   **Status:** Accepted
*   **Context:** The application needs to be scalable, portable, and aligned with modern cloud-native practices.
*   **Decision:** Use **Azure Kubernetes Service (AKS)** for production/stage and **Kind** for local development.
*   **Consequences:** Requires Helm charts for unified deployment logic across environments.

## 6. CI/CD: GitHub Actions
*   **Status:** Accepted
*   **Context:** We need an automated pipeline for testing, linting, building, and deploying.
*   **Decision:** Use **GitHub Actions**.
*   **Consequences:** Integrated directly with the source code repository.
