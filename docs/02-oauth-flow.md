# 02 — OAuth 2.0 Flow

## Interactive delegated flow used by this lab

```text
User
 |
 | sign in
 v
Microsoft Entra ID
 |
 | OAuth 2.0 access token
 v
MSAL PublicClientApplication
 |
 | Bearer token
 v
Microsoft Graph
 |
 +-- GET /v1.0/me
```

The application requests:

```text
User.Read
```

The token is used only to call the Graph resource.

## Production architecture

For an Azure-hosted autonomous agent, do not blindly copy the interactive public-client pattern.

Prefer:

- managed identity for Azure resources
- workload identity / federated credentials where appropriate
- confidential client credentials for appropriate server-to-server integrations
- least-privilege application permissions
- Conditional Access and privileged access controls for human/admin paths

## Interview explanation

> "OAuth 2.0 establishes the delegated authorization boundary. Entra authenticates the principal and issues a token containing the permitted scope. The agent presents that token to the target resource. I keep the Graph permission minimal and separate the identity used for telemetry ingestion from the identity used for Graph access."
