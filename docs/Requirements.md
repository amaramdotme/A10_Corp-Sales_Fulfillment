Overview
This document outlines the high-level requirements for a hypothetical Sales Fulfillment Application designed as a study exercise to explore Azure Kubernetes Services (AKS) implementation. The application captures client information in two phases—basic company details and engagement-specific details—before generating a unique Client ID. It serves as a front-end for service providers (e.g., similar to Liatrio, a DevOps consultancy) to streamline initial client onboarding. The focus is on applying DevOps and Site Reliability Engineering (SRE) principles while aligning with Azure's Well-Architected Framework pillars: Secure, Reliable, Performant, Operational Excellence, and Cost Optimized.
The application will be built as a modern, containerized web app deployed on AKS, emphasizing automation, scalability, and best practices for cloud-native development.
1. Business/Functional Requirements
These requirements define the core functionality from a business and user perspective, ensuring the app supports efficient client onboarding while minimizing manual intervention.

User Onboarding Workflow:
Provide a simple web-based form for clients to submit information in two sequential steps:
Basic company info: Company name, address, industry, contact person details (name, email, phone), and company size (e.g., employee count).
Engagement-specific info: Service type requested (e.g., DevOps consulting, cloud migration), project scope, timeline expectations, budget range, and any additional notes.

Validate inputs client-side and server-side to ensure completeness (e.g., required fields, email format).
Upon successful submission, automatically generate and display a unique Client ID (e.g., alphanumeric string) for tracking.

Data Handling and Integration:
Store submitted data in a backend database for retrieval by the service team.
Trigger a notification (e.g., email or internal system alert) to the service team upon submission, including the Client ID and a summary of the info.
Allow service team users (authenticated internal staff) to view and search submitted records via a basic admin dashboard.

User Experience:
Support multi-device access (web-responsive design for desktop and mobile).
Include basic error handling and user feedback (e.g., success messages, error prompts).
Ensure compliance with data privacy standards (e.g., GDPR-like principles for handling client data).

Non-Functional Business Aspects:
Handle up to 100 concurrent submissions during peak times without degradation.
Provide audit logs for submissions to support business accountability.


2. Technical Requirements
These requirements focus on the implementation using AKS, DevOps pipelines, and SRE practices. The design emphasizes high-level principles aligned with the five pillars, assuming a microservices architecture where the app is containerized (e.g., frontend in React/Node.js, backend in .NET/Python, database in Azure Cosmos DB or SQL).
General Technical Stack

Platform: Deploy on Azure Kubernetes Services (AKS) for orchestration of containerized workloads.
DevOps Tools: Use GitHub Actions for CI/CD pipelines; Infrastructure as Code (IaC) with Terraform or Bicep for provisioning AKS clusters.
SRE Principles: Implement SLIs/SLOs (e.g., 99.9% uptime), automated alerting, and chaos engineering for resilience testing.
Architecture: Stateless frontend pods, stateful backend services, and managed database; use Kubernetes namespaces for environment separation (dev, staging, prod).
Tech Stack: Frontend use Python FastHtml and Backend use FastAPI, also add libs for test driven development 

Enablement 
1. Local Workspace 
we need to use tools locally like Docker and kind to test the containerization aspect
2. Azure Landing zone 
There is already a repo that was used for creating a custom landing zone - https://github.com/amaramdotme/A10_Corp-terraform.git
3. Model FastHTML app 
Here is a local app that I had dabbled on in the past that uses Fasthtml, use it for reference, it might not be perfect - 
/home/wsladmin/dev/pyProjects/amaram_dev_landing

Pillar-Aligned Requirements
1. Secure

Implement Azure AD (Entra ID) for authentication and authorization (e.g., role-based access for clients vs. internal team).
Encrypt data in transit (HTTPS/TLS) and at rest (using Azure-managed keys).
Use Kubernetes secrets management and Azure Key Vault for sensitive data (e.g., API keys, connection strings).
Apply network security: AKS network policies, Azure Firewall, and private endpoints to restrict access.
Conduct automated vulnerability scanning in CI/CD pipelines (e.g., via Trivy or Azure Defender).

2. Reliable

Design for high availability: Multi-zone AKS node pools, pod replicas (e.g., 3+), and auto-scaling based on CPU/memory metrics.
Implement fault tolerance: Health probes, liveness/readiness checks, and circuit breakers in services.
Use managed Azure services for backend (e.g., Cosmos DB with geo-replication) to ensure data durability.
SRE Focus: Define SLOs for availability (e.g., 99.95%); use Azure Monitor for error budgeting and automated rollbacks in pipelines.

3. Performant

Optimize for low latency: Use AKS with Azure CNI networking, content delivery via Azure CDN for static assets.
Scale horizontally: Kubernetes Horizontal Pod Autoscaler (HPA) triggered by resource utilization or custom metrics (e.g., requests per second).
Efficient data handling: Asynchronous processing for notifications; caching (e.g., Redis on Azure Cache) for frequent reads.
Performance testing in DevOps: Integrate load testing (e.g., via Locust or Azure Load Testing) in CI/CD.

4. Operational Excellence

Automate deployments: GitOps with ArgoCD or Flux for declarative cluster management; zero-downtime updates via rolling deployments.
Monitoring and Logging: Azure Monitor, Prometheus/Grafana for metrics; Application Insights for tracing; centralized logging with ELK or Azure Log Analytics.
Incident Response: SRE playbooks for on-call rotations; automated alerts via Azure Alerts integrated with PagerDuty.
Observability: Implement distributed tracing and dashboards for end-to-end visibility.

5. Cost Optimized

Resource Efficiency: Right-size AKS nodes (e.g., spot instances for non-critical workloads); use Kubernetes Cluster Autoscaler to scale nodes dynamically.
Pay-as-You-Go: Leverage serverless components where possible (e.g., Azure Functions for notification triggers) to avoid idle costs.
Cost Monitoring: Use Azure Cost Management for budgeting; set up auto-shutdown for dev environments.
Optimization Practices: Regular audits via DevOps pipelines to identify and eliminate waste (e.g., oversized pods).








