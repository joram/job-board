import json
import os

import boto3


def load_secrets():
    client = boto3.client(
        service_name="secretsmanager",
        region_name="ca-central-1",
    )
    response = client.get_secret_value(SecretId="job_board_secrets")
    for key, value in json.loads(response["SecretString"]).items():
        os.environ[key] = value


try:
    load_secrets()
except Exception as e:
    print("No secrets found in Secrets Manager", e)


SLACK_CLIENT_ID = os.environ.get("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.environ.get("SLACK_CLIENT_SECRET")
SENTRY_DSN = os.environ.get("SENTRY_DSN")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

ADMIN_EMAILS = os.environ.get("ADMIN_EMAILS", "john.c.oram@gmail.com").split(",")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://localhost:3000")
