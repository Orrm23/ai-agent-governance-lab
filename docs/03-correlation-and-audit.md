# 03 — Invocation and Correlation

## Correlation ID generation

Every invocation gets:

```text
AGENT-<UUID>
```

Example:

```text
AGENT-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Propagation

The application sends:

```http
x-correlation-id: AGENT-<UUID>
```

to downstream calls.

The same value is written into the audit event.

## Audit schema

```json
{
  "TimeGenerated": "2026-10-05T19:24:00Z",
  "correlationId": "AGENT-EXAMPLE-UUID",
  "agentName": "UserLookupAgent",
  "user": "user@example.com",
  "operation": "READ_USER",
  "target": "https://graph.microsoft.com/v1.0/me",
  "statusCode": 200,
  "result": "SUCCESS"
}
```

## Why this matters

A correlation ID allows an investigator to start from an agent invocation and trace:

```text
Agent invocation
 -> identity/token acquisition
 -> downstream request
 -> authorization result
 -> audit event
 -> Log Analytics
 -> Sentinel investigation
```

## Important distinction

The custom application correlation ID is not the same thing as native Entra request/correlation IDs.

In a production design, preserve both when available.
