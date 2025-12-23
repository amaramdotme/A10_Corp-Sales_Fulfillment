import subprocess
import json
import re

RESOURCE_GROUP = "rg-root-iac"
WORKSPACE_NAME = "log-a10corp-hq"
CATEGORY = "A10_SalesFulfillment" # Updated category name as well

# Define base queries and their chart variants
# Display names will now start with a10_
queries = {
    "a10_App Logs (All)": """ContainerLog
| where LogEntrySource == "stdout" or LogEntrySource == "stderr"
| extend ContainerName = extract("([^/]+)$", 1, ContainerID)
| project TimeGenerated, LogEntry, ContainerName, LogEntrySource
| sort by TimeGenerated desc""",

    "a10_App Logs (All) Chart": """ContainerLog
| where LogEntrySource == "stdout" or LogEntrySource == "stderr"
| extend ContainerName = extract("([^/]+)$", 1, ContainerID)
| summarize LogCount = count() by bin(TimeGenerated, 5m), ContainerName
| render columnchart with (kind=stacked)""",

    "a10_App Logs (Table)": """let env_namespace = "sales-fulfillment-prod";
KubePodInventory
| where Namespace == env_namespace
| project ContainerID, PodName = Name, Namespace
| join kind=inner (
    ContainerLog
    | extend ContainerName = extract("([^/]+)$", 1, ContainerID)
) on ContainerID
| project TimeGenerated, Namespace, PodName, LogEntry
| sort by TimeGenerated desc""",

    "a10_App Logs (Chart)": """let env_namespace = "sales-fulfillment-prod";
KubePodInventory
| where Namespace == env_namespace
| project ContainerID, PodName = Name, Namespace
| join kind=inner (
    ContainerLog
    | extend ContainerName = extract("([^/]+)$", 1, ContainerID)
) on ContainerID
| summarize LogCount = count() by bin(TimeGenerated, 5m), PodName
| render columnchart with (kind=stacked)""",

    "a10_Error Tracking": """ContainerLog
| where LogEntry contains "ERROR" or LogEntry contains "Exception" or LogEntry contains "500"
| extend ContainerName = extract("([^/]+)$", 1, ContainerID)
| project TimeGenerated, LogEntry, ContainerName
| sort by TimeGenerated desc""",

    "a10_Error Tracking Chart": """ContainerLog
| where LogEntry contains "ERROR" or LogEntry contains "Exception" or LogEntry contains "500"
| extend ContainerName = extract("([^/]+)$", 1, ContainerID)
| summarize ErrorCount = count() by bin(TimeGenerated, 5m), ContainerName
| render timechart""",

    "a10_Pod Restarts": """KubePodInventory
| where ContainerRestartCount > 0
| summarize MaxRestartCount = max(ContainerRestartCount) by Name, Namespace, ControllerName
| where MaxRestartCount > 0
| order by MaxRestartCount desc""",

    "a10_Pod Restarts Chart": """KubePodInventory
| where ContainerRestartCount > 0
| summarize MaxRestartCount = max(ContainerRestartCount) by bin(TimeGenerated, 30m), Name
| render timechart""",

    "a10_CPU and Memory Chart": """Perf
| where ObjectName == "K8SContainer"
| where CounterName == "cpuUsageNanoCores" or CounterName == "memoryWorkingSetBytes"
| extend InstanceName = extract("([^/]+)$", 1, InstanceName)
| summarize AverageValue = avg(CounterValue) by CounterName, InstanceName, bin(TimeGenerated, 1h)
| render timechart""",

    "a10_Backend Health Chart": """ContainerLog
| where LogEntry contains "GET /health"
| summarize count() by bin(TimeGenerated, 5m)
| render timechart""",

    "a10_Network Traffic Chart": """Perf
| where ObjectName == "K8SContainer"
| where CounterName == "networkRxBytes" or CounterName == "networkTxBytes"
| extend InstanceName = extract("([^/]+)$", 1, InstanceName)
| summarize TotalBytes = sum(CounterValue) by CounterName, InstanceName, bin(TimeGenerated, 1h)
| render timechart""",

    "a10_Internal DNS Failures": """KubePodInventory
| where Namespace == "kube-system" and Name contains "coredns"
| join kind=inner (
    ContainerLog
    | where LogEntry contains "ERROR" or LogEntry contains "SERVFAIL"
) on ContainerID
| project TimeGenerated, LogEntry""",

    "a10_Internal DNS Failures Chart": """KubePodInventory
| where Namespace == "kube-system" and Name contains "coredns"
| join kind=inner (
    ContainerLog
    | where LogEntry contains "ERROR" or LogEntry contains "SERVFAIL"
) on ContainerID
| summarize FailureCount = count() by bin(TimeGenerated, 5m)
| render timechart"""
}

def create_saved_search(name, query):
    # Sanitize name for ID (remove all non-alphanumeric characters, must start with letter)
    search_id = re.sub(r'[^a-zA-Z0-9]', '', name)
    
    cmd = [
        "az", "monitor", "log-analytics", "workspace", "saved-search", "create",
        "--resource-group", RESOURCE_GROUP,
        "--workspace-name", WORKSPACE_NAME,
        "--name", search_id,
        "--display-name", name,
        "--category", CATEGORY,
        "--saved-query", query
    ]
    
    print(f"Creating/Updating query: {name}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully created '{name}'")
        else:
            print(f"Failed to create '{name}':")
            print(result.stderr)
    except Exception as e:
        print(f"Error executing command for '{name}': {e}")

# First, attempt to delete existing ones in the old category if possible, 
# but simply creating new ones with the prefix is cleaner for finding them.
for name, query in queries.items():
    create_saved_search(name, query)