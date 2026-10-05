# 01 — App Registrations

## App registration 1: AI-Agent-Demo

Create an Entra ID App Registration for the agent.

Recommended lab settings:

- Name: `AI-Agent-Demo`
- Supported account type: accounts in this organizational directory
- Authentication: Mobile and desktop applications
- Redirect URI: `http://localhost`
- Public client flows: enabled for this interactive lab
- API permissions:
  - Microsoft Graph
  - Delegated
  - `User.Read`

Grant admin consent only when required by tenant policy.

### Why `User.Read`?

The lab calls `/me`. It does not need tenant-wide directory permissions.

Avoid broad permissions such as `Directory.ReadWrite.All` unless a documented business requirement exists.

## App registration 2: AI-Agent-Log-Ingest

Create a separate application identity for the Logs Ingestion API.

Purpose:

- authenticate the ingestion process
- write logs through the DCR

It does not need Microsoft Graph permissions.

For production, prefer a managed identity for an Azure-hosted ingestion workload where supported.

If a client secret is used for the lab:

- copy the secret **Value**, not Secret ID
- store it as an environment variable
- never commit it

## Separation of duties

```text
AI-Agent-Demo
  └── Graph access

AI-Agent-Log-Ingest
  └── Azure Monitor ingestion access
```

This prevents the ingestion identity from inheriting unnecessary Graph permissions.
