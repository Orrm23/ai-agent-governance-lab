import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import msal
import requests


# Fill these from your Entra App Registration.
CLIENT_ID = "YOUR_AI_AGENT_APP_CLIENT_ID"
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["User.Read"]

GRAPH_URL = "https://graph.microsoft.com/v1.0/me"
AGENT_NAME = "UserLookupAgent"
OPERATION = "READ_USER"

AUDIT_FILE = Path("agent-audit.jsonl")


def main():
    correlation_id = f"AGENT-{uuid.uuid4()}"
    timestamp = datetime.now(timezone.utc).isoformat()

    print("===================================")
    print("AI AGENT INVOCATION")
    print("===================================")
    print(f"Agent:           {AGENT_NAME}")
    print(f"Correlation ID:  {correlation_id}")
    print(f"Operation:       {OPERATION}")
    print(f"Timestamp:       {timestamp}")
    print("===================================")

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
    )

    result = app.acquire_token_interactive(scopes=SCOPES)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Authentication failed"))

    token = result["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "x-correlation-id": correlation_id,
    }

    response = requests.get(GRAPH_URL, headers=headers, timeout=30)

    claims = result.get("id_token_claims", {})
    user = claims.get("preferred_username", claims.get("upn", "unknown"))

    audit_event = {
        "TimeGenerated": timestamp,
        "correlationId": correlation_id,
        "agentName": AGENT_NAME,
        "user": user,
        "operation": OPERATION,
        "target": GRAPH_URL,
        "statusCode": response.status_code,
        "result": "SUCCESS" if response.ok else "ERROR",
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(audit_event) + "\n")

    print(f"HTTP Status: {response.status_code}")
    print(f"Result:      {audit_event['result']}")
    print(f"Audit file:  {AUDIT_FILE}")

    print("\nGRAPH RESPONSE")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
