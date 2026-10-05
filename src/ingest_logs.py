import json
import os
from pathlib import Path

from azure.identity import ClientSecretCredential
from azure.monitor.ingestion import LogsIngestionClient


TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]

DCE_ENDPOINT = os.environ["DCE_ENDPOINT"]
DCR_IMMUTABLE_ID = os.environ["DCR_IMMUTABLE_ID"]
STREAM_NAME = os.environ.get("STREAM_NAME", "Custom-AgentInvocation_CL")

LOG_FILE = Path("agent-audit.jsonl")


def main():
    if not LOG_FILE.exists():
        raise FileNotFoundError(LOG_FILE)

    records = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    if not records:
        raise RuntimeError("No audit events found.")

    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )

    client = LogsIngestionClient(
        endpoint=DCE_ENDPOINT,
        credential=credential,
    )

    client.upload(
        rule_id=DCR_IMMUTABLE_ID,
        stream_name=STREAM_NAME,
        logs=records,
    )

    print(f"Uploaded {len(records)} audit event(s) successfully.")


if __name__ == "__main__":
    main()
