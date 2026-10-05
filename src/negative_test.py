import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import msal
import requests


CLIENT_ID = "YOUR_AI_AGENT_APP_CLIENT_ID"
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["User.Read"]

# Safe read-only test. It normally requires additional directory permissions.
GRAPH_URL = "https://graph.microsoft.com/v1.0/users"

AGENT_NAME = "UserLookupAgent"
OPERATION = "READ_USERS_UNAUTHORIZED"
AUDIT_FILE = Path("agent-audit.jsonl")


def main():
    correlation_id = f"AGENT-{uuid.uuid4()}"
    timestamp = datetime.now(timezone.utc).isoformat()

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
    )

    result = app.acquire_token_interactive(scopes=SCOPES)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Authentication failed"))

    headers = {
        "Authorization": f"Bearer {result['access_token']}",
        "x-correlation-id": correlation_id,
    }

    response = requests.get(GRAPH_URL, headers=headers, timeout=30)

    if response.status_code == 403:
        audit_result = "DENIED"
    elif response.status_code == 200:
        audit_result = "UNEXPECTED_SUCCESS"
    else:
        audit_result = "ERROR"

    claims = result.get("id_token_claims", {})
    user = claims.get("preferred_username", claims.get("upn", "unknown"))

    event = {
        "TimeGenerated": timestamp,
        "correlationId": correlation_id,
        "agentName": AGENT_NAME,
        "user": user,
        "operation": OPERATION,
        "target": GRAPH_URL,
        "statusCode": response.status_code,
        "result": audit_result,
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    print("===================================")
    print("NEGATIVE AUTHORIZATION TEST")
    print("===================================")
    print(f"HTTP Status: {response.status_code}")
    print(f"Result:      {audit_result}")
    print(f"Correlation: {correlation_id}")
    print("===================================")


if __name__ == "__main__":
    main()
