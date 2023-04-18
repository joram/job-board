from uuid import uuid4

import settings


def prefixed_uuid(prefix: str) -> str:
    return str(prefix + str(uuid4()))


def frontend_url(path: str) -> str:
    return f"{settings.FRONTEND_URL}{path}"
