from uuid import uuid4


def prefixed_uuid(prefix: str) -> str:
    return prefix + str(uuid4())
