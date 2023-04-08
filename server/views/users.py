import datetime

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class LoginResponse(BaseModel):
    token: str
    user: User


@router.post("/login", tags=["public"])
async def post_login() -> LoginResponse:
    requests.get



