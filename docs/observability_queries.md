# Observability Queries (KQL)

This document contains useful Kusto Query Language (KQL) queries for monitoring the Sales Fulfillment application in the Azure Portal (Log Analytics).

## How to Use
1. Go to the [Azure Portal](https://portal.azure.com).
2. Search for **Log Analytics Workspaces**.
3. Select `log-a10corp-hq`.
4. Click on **Logs** in the left sidebar.
5. Paste any of these queries into the editor and click **Run**.

---

## 1. Application Logs (All Environments)
See all stdout/stderr logs from the frontend and backend across all environments.

```kql
ContainerLog
| where LogEntrySource == "stdout" or LogEntrySource == "stderr"
| extend ContainerName = extract("([^/]+)$", 1, ContainerID)
| project TimeGenerated, LogEntry, ContainerName, LogEntrySource
| sort by TimeGenerated desc
```

## 2. Environment-Specific Logs
Filter logs for a specific environment (e.g., `prod`).

```kql
let env_namespace = "sales-fulfillment-prod"; // Change to -stage or sales-fulfillment for dev
KubePodInventory
| where Namespace == env_namespace
| project ContainerID, PodName = Name, Namespace
| join kind=inner (
    ContainerLog
    | extend ContainerName = extract("([^/]+)$", 1, ContainerID)
) on ContainerID
| project TimeGenerated, Namespace, PodName, LogEntry
| sort by TimeGenerated desc
```

## 3. Error Tracking
Find specific errors or exceptions across the entire application.

```kql
ContainerLog
| where LogEntry contains "ERROR" or LogEntry contains "Exception" or LogEntry contains "500"
| extend ContainerName = extract("([^/]+)$", 1, ContainerID)
| project TimeGenerated, LogEntry, ContainerName
| sort by TimeGenerated desc
```

## 4. Pod Restart Monitoring
Identify pods that are crashing or restarting frequently.

```kql
KubePodInventory
| where ContainerRestartCount > 0
| summarize MaxRestartCount = max(ContainerRestartCount) by Name, Namespace, ControllerName
| where MaxRestartCount > 0
| order by MaxRestartCount desc
```

## 5. CPU and Memory Usage (Last 24 Hours)
View the resource consumption of your frontend and backend pods.

```kql
Perf
| where ObjectName == "K8SContainer"
| where CounterName == "cpuUsageNanoCores" or CounterName == "memoryWorkingSetBytes"
| extend InstanceName = extract("([^/]+)$", 1, InstanceName)
| summarize AverageValue = avg(CounterValue) by CounterName, InstanceName, bin(TimeGenerated, 1h)
| render timechart
```

## 6. Backend Performance (Health Checks)
Monitor the backend health endpoint logs.

```kql
ContainerLog
| where LogEntry contains "GET /health"
| summarize count() by bin(TimeGenerated, 5m)
| render timechart

## 7. Network Traffic Monitoring (Per Container)
Monitor the amount of network traffic (bytes) sent and received by your frontend/backend containers.

```kql
Perf
| where ObjectName == "K8SContainer"
| where CounterName == "networkRxBytes" or CounterName == "networkTxBytes"
| extend InstanceName = extract("([^/]+)$", 1, InstanceName)
| summarize TotalBytes = sum(CounterValue) by CounterName, InstanceName, bin(TimeGenerated, 1h)
| render timechart
```

## 8. Load Balancer & Connection Health
To view Load Balancer specific metrics (like SNAT port exhaustion or VIP availability), it is best to check the **Azure Load Balancer** resource directly in the portal under the **Metrics** blade.

However, you can check for internal DNS failures within the cluster using this query:

```kql
KubePodInventory
| where Namespace == "kube-system" and Name contains "coredns"
| join kind=inner (
    ContainerLog
    | where LogEntry contains "ERROR" or LogEntry contains "SERVFAIL"
) on ContainerID
| project TimeGenerated, LogEntry
```
```
