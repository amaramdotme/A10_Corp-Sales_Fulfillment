# Azure Resource List (A10 Corp) - created by platform / foundation repo
https://github.com/amaramdotme/A10_Corp-terraform

Generated on: 2025-12-20

## 1. Global / Root Infrastructure
**Subscription:** `sub-root` (fdb297a9-2ece-469c-808d-a8227259f6e8)

| Resource Name | Resource Type | Purpose |
|---------------|---------------|---------|
| `rg-root-iac` | Resource Group | Root Infrastructure Management |
| `storerootblob` | Storage Account | Terraform Remote State Backend |
| `kv-root-terraform` | Key Vault | Root Secret Management |
| `acra10corpsales` | Container Registry | Global Shared Artifact Repository |
| `log-a10corp-hq` | Log Analytics Workspace | Centralized Monitoring & Forensics Sink |

## 2. Foundation (Organizational Hierarchy)
**Tenant:** `8116fad0-5032-463e-b911-cc6d1d75001d`

### Management Groups
| Management Group Name | Display Name |
|-----------------------|--------------|
| `mg-a10corp` | Tenant Root / A10 Corp |
| `mg-a10corp-hq` | HQ Management Group |
| `mg-a10corp-sales` | Sales Management Group |
| `mg-a10corp-service` | Service Management Group |

### Governance Policies (Assigned to mg-a10corp-hq)
| Policy Assignment Name | Definition | Scope | Effect |
|------------------------|------------|-------|--------|
| `enforce-env-tag` | Require a tag on resource groups | Resource Groups | Deny |
| `allowed-locations` | Allowed locations | Resources | Deny (except `eastus`, `eastus2`) |
| `allowed-vm-skus` | Allowed virtual machine size SKUs | Virtual Machines | Deny (B, D series only) |
| `secure-transfer` | Secure transfer to storage accounts | Storage Accounts | Deny |

## 3. Workloads (Environment: dev)

### Sales Workload (Dev)
**Subscription:** `sub-sales` (385c6fcb-c70b-4aed-b745-76bd608303d7)

| Resource Name | Resource Type | Details | Status |
|---------------|---------------|---------|--------|
| `rg-a10corp-sales-dev` | Resource Group | Workload Container | ✅ Deployed |
| `id-a10corp-sales-dev` | User Assigned Identity | AKS Control Plane Identity | ✅ Deployed |
| `vnet-a10corp-sales-dev` | Virtual Network | 10.0.0.0/16 | ✅ Deployed |
| `snet-a10corp-sales-dev-aks-nodes` | Subnet | 10.0.1.0/24 | ✅ Deployed |
| `snet-a10corp-sales-dev-ingress` | Subnet | 10.0.2.0/24 | ✅ Deployed |
| `nsg-a10corp-sales-dev-aks-nodes` | NSG | Default Security | ✅ Deployed |
| `nsg-a10corp-sales-dev-ingress` | NSG | Allows HTTP/HTTPS | ✅ Deployed |
| `route-a10corp-sales-dev` | Route Table | Default Route (Internet) | ✅ Deployed |

## 4. Workloads (Environment: stage)

### Sales Workload (Stage)
**Subscription:** `sub-sales` (385c6fcb-c70b-4aed-b745-76bd608303d7)

| Resource Name | Resource Type | Details | Status |
|---------------|---------------|---------|--------|
| `rg-a10corp-sales-stage` | Resource Group | Workload Container | ✅ Deployed |
| `id-a10corp-sales-stage` | User Assigned Identity | AKS Control Plane Identity | ✅ Deployed |
| `vnet-a10corp-sales-stage` | Virtual Network | 10.0.0.0/16 | ✅ Deployed |
| `snet-a10corp-sales-stage-aks-nodes` | Subnet | 10.0.1.0/24 | ✅ Deployed |
| `snet-a10corp-sales-stage-ingress` | Subnet | 10.0.2.0/24 | ✅ Deployed |
| `nsg-a10corp-sales-stage-aks-nodes` | NSG | Default Security | ✅ Deployed |
| `nsg-a10corp-sales-stage-ingress` | NSG | Allows HTTP/HTTPS | ✅ Deployed |
| `route-a10corp-sales-stage` | Route Table | Default Route (Internet) | ✅ Deployed |

## 5. Workloads (Environment: prod)

### Sales Workload (Prod)
**Subscription:** `sub-sales` (385c6fcb-c70b-4aed-b745-76bd608303d7)

| Resource Name | Resource Type | Details | Status |
|---------------|---------------|---------|--------|
| `rg-a10corp-sales-prod` | Resource Group | Workload Container | ✅ Deployed |
| `id-a10corp-sales-prod` | User Assigned Identity | AKS Control Plane Identity | ✅ Deployed |
| `vnet-a10corp-sales-prod` | Virtual Network | 10.0.0.0/16 | ✅ Deployed |
| `snet-a10corp-sales-prod-aks-nodes` | Subnet | 10.0.1.0/24 | ✅ Deployed |
| `snet-a10corp-sales-prod-ingress` | Subnet | 10.0.2.0/24 | ✅ Deployed |
| `nsg-a10corp-sales-prod-aks-nodes` | NSG | Default Security | ✅ Deployed |
| `nsg-a10corp-sales-prod-ingress` | NSG | Allows HTTP/HTTPS | ✅ Deployed |
| `route-a10corp-sales-prod` | Route Table | Default Route (Internet) | ✅ Deployed |

## 6. Identities & Access
This section tracks identities used for automation and workload security.

### Terraform-Managed (Workload Identities)
| Identity Name | Type | Subscription | Purpose |
|---------------|------|--------------|---------|
| `id-a10corp-sales-dev` | Managed Identity | `sub-sales` | AKS Control Plane (AcrPull) |
| `id-a10corp-sales-stage` | Managed Identity | `sub-sales` | AKS Control Plane (AcrPull) |
| `id-a10corp-sales-prod` | Managed Identity | `sub-sales` | AKS Control Plane (AcrPull) |

### Manually Created (CI/CD & Management)
| Identity Name | Type | Purpose |
|---------------|------|---------|
| `github-oidc-a10-corp-terraform` | Service Principal | GitHub Actions OIDC Authentication |
| `github-actions-terraform-a10corp` | Service Principal | Legacy or Backup CI/CD Identity |

## 7. System / Automatically Created Resources
These resources were created automatically by Azure.

| Resource Name | Resource Type | Subscription | Purpose |
|---------------|---------------|--------------|---------|
| `NetworkWatcherRG` | Resource Group | `sub-sales` | Container for network monitoring tools |
| `NetworkWatcher_eastus` | Network Watcher | `sub-sales` | Regional network monitoring service |