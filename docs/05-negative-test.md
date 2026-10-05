# 05 — Negative Authorization Test

## Goal

Prove that the agent cannot perform an operation outside its granted authorization boundary.

The positive test calls:

```text
GET /v1.0/me
```

using:

```text
User.Read
```

The negative test attempts:

```text
GET /v1.0/users
```

without adding broad directory permissions.

Expected outcome:

```text
HTTP 403
result = DENIED
```

## Why this is important

A governance control is stronger when the evidence demonstrates both:

- authorized action succeeds
- unauthorized action is blocked

## Evidence

The negative event should contain:

```json
{
  "correlationId": "AGENT-...",
  "operation": "READ_USERS_UNAUTHORIZED",
  "statusCode": 403,
  "result": "DENIED"
}
```

Do not use destructive APIs for a governance test.
