from fastapi import Header, HTTPException


async def verify_auth_token(auth_token: str = Header(default=None)) -> None:
    if auth_token not in ["valid_auth_token"]:
        raise HTTPException(status_code=403, detail="Invalid Auth Token")
