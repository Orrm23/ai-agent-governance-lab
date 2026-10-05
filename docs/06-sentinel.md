# 06 — Microsoft Sentinel

## Workspace

Connect Microsoft Sentinel to the Log Analytics workspace containing `AgentInvocation_CL`.

## Starter detection

Use the custom audit table to identify denied agent operations:

```kusto
AgentInvocation_CL
| where result == "DENIED"
| project TimeGenerated, correlationId, agentName, user, operation, target, statusCode
| order by TimeGenerated desc
```

## Correlation investigation

```kusto
AgentInvocation_CL
| where correlationId == "AGENT-EXAMPLE-UUID"
| order by TimeGenerated asc
```

## Production evolution

A mature implementation can add:

- analytic rules
- incident creation
- automation/playbooks
- identity risk context
- Defender signals
- privileged operation monitoring
- anomaly detection
- agent-specific allow/deny policies
- retention and evidence controls

## Governance mapping

| Control | Evidence |
|---|---|
| Identity | Entra App Registration |
| Authorization | Least-privilege Graph permission |
| Invocation traceability | Application correlation ID |
| Auditability | Structured JSON event |
| Central logging | Log Analytics custom table |
| Detection | Sentinel KQL rule |
| Negative assurance | 403 denied-operation test |
