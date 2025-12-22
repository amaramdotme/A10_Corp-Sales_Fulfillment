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

## 7. Authentication: GitHub OIDC (Keyless)
*   **Status:** Accepted (2025-12-21)
*   **Context:** We need a secure way for GitHub Actions to authenticate with Azure without storing long-lived Client Secrets (passwords).
*   **Decision:** Use **GitHub OIDC Federated Identity**.
*   **Consequences:** Improves security posture. Requires one-time manual setup of Federated Credentials in Azure AD for each GitHub Environment.

## 8. Kubernetes Version Selection (LTS vs. Official)
*   **Status:** Accepted (2025-12-21)
*   **Context:** Azure AKS now designates certain versions (like 1.29, 1.30) as LTS, which are restricted to Premium tiers or specific support plans.
*   **Decision:** Target **KubernetesOfficial** versions (e.g., 1.32) for Dev/Stage environments to remain on the standard/free tier.
*   **Consequences:** Requires more frequent version bumps but avoids Premium tier costs for non-production environments.

## 9. VM SKU Selection (D-Series for Stability)
*   **Status:** Accepted (2025-12-21)
*   **Context:** B-Series burstable instances (like B2s) can have restricted availability or quota limitations in certain regions (e.g., eastus).
*   **Decision:** Prefer **Standard_D2s_v3** (D-Series) for AKS nodes.
*   **Consequences:** Slightly higher cost than B-series, but provides consistent performance and significantly better regional availability/quota support.

## 10. Database Backend: Azure SQL
*   **Status:** Accepted (2025-12-21)
*   **Context:** The application needs a scalable, managed database for production environments. SQLite is used for local development and testing.
*   **Decision:** Use **Azure SQL (Single Database)**.
*   **Reasoning:** Provides a fully managed, relational database that integrates seamlessly with Azure Managed Identities and Virtual Networks.
*   **Consequences:** Requires installing MSSQL ODBC drivers in the backend container image and updating the application to handle SQLAlchemy's `mssql+pyodbc` connection strings.

## 11. FastHTML Live Reload Configuration
*   **Status:** Accepted (2025-12-21)
*   **Context:** FastHTML's `live=True` feature causes an infinite refresh loop when accessed through an Azure Load Balancer.
*   **Decision:** Disable `live` reload by default and make it configurable via the `LIVE_RELOAD` environment variable.
*   **Consequences:** Prevents routing issues in deployed environments while maintaining development productivity in local Kind clusters.

## 12. Blue/Green Production Deployment Strategy
*   **Status:** Accepted (2025-12-22)
*   **Context:** Production deployments should be zero-downtime and easy to roll back if failures occur during startup or data migration.
*   **Decision:** Use a Blue/Green strategy with a manual promotion gate.
    *   **Phase 1 (Green):** CI/CD deploys a parallel Helm release (`sales-app-green`) to the production namespace.
    *   **Phase 2 (Switch):** A manual workflow (`promote-to-prod.yml`) upgrades the main `sales-app` release to the new images and uninstalls the green release.
*   **Reasoning:** Minimizes risk by validating the "Green" version in the real production environment before making it user-facing.

## 13. Azure Service Endpoints for Blob Storage Access
*   **Status:** Accepted (2025-12-22)
*   **Context:** AKS pods need to write JSON backups to Azure Blob Storage. Storage account has restrictive network rules (default deny) for security. IP-based allowlisting doesn't work well for dynamic AKS pod IPs.
*   **Decision:** Use **Azure Service Endpoints** to enable secure connectivity from AKS subnet to storage account.
    *   Enable `Microsoft.Storage` service endpoint on AKS node subnet
    *   Configure storage account to allow traffic from AKS subnet via VNet rules
    *   Use managed identity (kubelet identity) for authentication (Storage Blob Data Contributor role)
*   **Reasoning:**
    *   Traffic stays on Azure backbone (secure, private, no public internet)
    *   No need to manage dynamic IP allowlists
    *   Works across subscriptions (storage in `sub-root`, AKS in `sub-sales`)
    *   Maintains storage account's restrictive firewall (deny by default)
*   **Consequences:**
    *   **Temporary Implementation:** Due to poly-repo architecture, configuration is temporarily in Workload repo
    *   **TODO:** Move to Foundation repo - Platform team should own storage network rules and subnet service endpoints
    *   Portal access to storage requires manual IP allowlisting or temporarily setting `defaultAction: Allow`
