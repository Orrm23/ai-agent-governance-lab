# AI Agent Governance — Architect Runbook

## 1. Business objective

Provide an auditable identity and authorization boundary for AI-agent activity while maintaining end-to-end traceability.

## 2. Trust boundaries

### Boundary A — Human to Entra

Human authentication is handled by Microsoft Entra ID.

### Boundary B — Agent to resource

The agent uses an OAuth 2.0 access token with explicitly granted scopes/roles.

### Boundary C — Agent to telemetry

Telemetry uses a separate workload identity and Azure Monitor ingestion path.

This separation is intentional: an identity that can read business data should not automatically be granted telemetry administration privileges.

## 3. Identity architecture

```text
                +----------------------+
                | Microsoft Entra ID   |
                +----------+-----------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
     AI-Agent-Demo              AI-Agent-Log-Ingest
     Graph identity             Telemetry identity
             |                           |
             v                           v
      Microsoft Graph            Azure Monitor
                                   DCE / DCR
```

## 4. OAuth authorization

The lab demonstrates delegated authorization with `User.Read`.

The architecture deliberately avoids broad directory permissions.

For an autonomous Azure-hosted production agent, evaluate managed identity, workload identity and application permissions based on the actual resource/API model.

## 5. Invocation lifecycle

```text
1. Agent receives request
2. Agent generates correlation ID
3. Agent authenticates
4. Agent obtains access token
5. Agent calls downstream resource
6. Agent records status
7. Agent emits structured audit event
8. Ingestion identity sends event to Azure Monitor
9. DCR routes event to Log Analytics
10. Sentinel detects policy-relevant behavior
```

## 6. Evidence model

For every control maintain:

- control design
- operating procedure
- positive test
- negative test
- timestamped evidence
- correlation identifier
- responsible owner

## 7. Interview answer

> "I approached agent governance as an identity, authorization and observability problem. I separated the agent identity from the telemetry ingestion identity, used Entra ID and OAuth 2.0 with least privilege, generated an application correlation ID for every invocation, propagated it downstream, and emitted structured audit events. Azure Monitor Logs Ingestion routed those events through a DCE and DCR into a custom Log Analytics table. The same correlation ID is then used for investigation and Sentinel detections. I also designed positive and negative authorization tests so the control is evidenced rather than only documented."

## 8. Production hardening backlog

- Managed identity / workload identity
- PIM for privileged administration
- Conditional Access for human access
- Key Vault for secret management where secrets remain necessary
- Private/network-controlled ingestion path
- Sentinel analytics and automation
- RBAC separation of duties
- CI/CD security scanning
- schema/version governance
- retention and evidence policy
- alert tuning and incident response
