# 04 — Azure Monitor Log Ingestion

## Components

```text
Application
   |
   v
Logs Ingestion API
   |
   v
Data Collection Endpoint (DCE)
   |
   v
Data Collection Rule (DCR)
   |
   v
Log Analytics Workspace
   |
   v
AgentInvocation_CL
```

## Stream

The lab DCR uses:

```text
Custom-AgentInvocation_CL
```

The stream name in the Python client must exactly match the stream configured in the live DCR.

## Environment variables

```powershell
$env:AZURE_TENANT_ID="..."
$env:AZURE_CLIENT_ID="..."
$env:AZURE_CLIENT_SECRET="..."
$env:DCE_ENDPOINT="https://..."
$env:DCR_IMMUTABLE_ID="..."
$env:STREAM_NAME="Custom-AgentInvocation_CL"
```

## Query

```kusto
AgentInvocation_CL
| sort by TimeGenerated desc
| take 20
```

## Investigation by correlation ID

```kusto
AgentInvocation_CL
| where correlationId == "AGENT-EXAMPLE-UUID"
| order by TimeGenerated asc
```

If your deployed table exposes type suffixes in the query experience, use the exact column names shown by the table schema.
