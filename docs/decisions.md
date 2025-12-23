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
*   **Status:** Superseded (2025-12-21)
*   **Context:** The application was initially planned to use Azure SQL for production.
*   **Decision:** Revert to **SQLite with Azure Blob Storage backups**.
*   **Reasoning:** 
    *   Significant reduction in architectural complexity for the initial pilot.
    *   Avoids managing complex SQL connection strings and drivers.
    *   Durability is achieved via JSON backups to highly available blob storage.
    *   Alignment with organization's current preference for cost-efficient, simplified storage for this scale.
*   **Consequences:** Limits the application to a single backend replica (see Decision 14).

## 11. FastHTML Live Reload Configuration
*   **Status:** Accepted (2025-12-21)
*   **Context:** FastHTML's `live=True` feature causes an infinite refresh loop when accessed through an Azure Load Balancer.
*   **Decision:** Disable `live` reload by default and make it configurable via the `LIVE_RELOAD` environment variable.
*   **Consequences:** Prevents routing issues in deployed environments while maintaining development productivity in local Kind clusters.

## 12. Direct Production Deployment Strategy (Replacing Blue/Green)
*   **Status:** Accepted (2025-12-22)
*   **Context:** The initial plan for Blue/Green deployment proved complex for a single-replica SQLite-based application. Using a parallel "Green" release caused resource contention and complexity with persistent volume claims.
*   **Decision:** Revert to a **Direct Deployment** strategy (same as Stage).
    *   **Workflow:** The `deploy-prod` job directly upgrades the existing Helm release (`sales-app`).
    *   **Strategy:** Uses `type: Recreate` (from Decision 14) to ensure the old pod terminates and releases the volume lock before the new one starts.
*   **Reasoning:**
    *   Simplifies the CI/CD pipeline significantly.
    *   Avoids PVC/Multi-Attach errors inherent to running parallel deployments with ReadWriteOnce volumes.
    *   The brief downtime (seconds) during the `Recreate` phase is acceptable for this internal tool's SLA.

## 13. Storage Account Network Access Strategy
*   **Status:** Accepted (2025-12-22)
*   **Context:** AKS pods need to write JSON backups to Azure Blob Storage. Initial investigation showed storage account with restrictive network rules (default deny).
*   **Decision:** Foundation team configured storage account to **match Terraform state storage** (`storerootblob`):
    *   `defaultAction: Allow` (permissive, simplified)
    *   `bypass: AzureServices`
    *   Authentication via managed identity (Storage Blob Data Contributor role)
*   **Reasoning:** Simplifies the stack and aligns with the organization's existing storage patterns for shared accounts.

## 14. Backend Replica Limit and Deployment Strategy (SQLite Compatibility)
*   **Status:** Accepted (2025-12-22)
*   **Context:** Using SQLite with a standard ReadWriteOnce (RWO) persistent volume prevents multiple pods from concurrently mounting the volume. Standard `RollingUpdate` attempts to start a new pod before killing the old one, causing a deadlock.
*   **Decision:** 
    *   Hard-limit the backend to **1 replica** in all environments.
    *   Set the Deployment strategy to **`type: Recreate`**.
*   **Consequences:**
    *   Ensures the old pod is terminated (releasing the volume lock) before the new pod starts.
    *   Causes a brief period of downtime (seconds) during deployments.
    *   Fixes the "Multi-Attach" deadlock issue permanently for SQLite-based workloads.
    *   Horizontal scaling or zero-downtime updates would require migration to a shared database (e.g., PostgreSQL/Azure SQL).

## 15. Observability: Azure Monitor for Containers (OMS Agent)
*   **Status:** Accepted (2025-12-22)
*   **Context:** We need centralized logging and metrics for troubleshooting and performance monitoring.
*   **Decision:** Enable the **OMS Agent** (Container Insights) on all AKS clusters, pointing to the centralized `log-a10corp-hq` Log Analytics Workspace.
*   **Consequences:** Provides automatic collection of stdout/stderr logs and cluster metrics without requiring sidecars or application-level changes.
