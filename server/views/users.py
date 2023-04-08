import datetime
from typing import Optional

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import settings

router = APIRouter()


class User(BaseModel):
    id: str
    profile_picture: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class LoginResponse(BaseModel):
    token: str
    user: User


class AuthedUser(BaseModel):
    id: str
    scope: str
    access_token: str
    token_type: str


class Team(BaseModel):
    id: str


class SlackAuthResponse(BaseModel):
    ok: bool
    app_id: str
    authed_user: AuthedUser
    team: Team
    enterprise: Optional[str]
    is_enterprise_install: bool


class SlackOpenIdConnectUserInfo(BaseModel):
    ok: bool
    name: str
    picture: str


@router.get("/login", tags=["public"])
async def get_login(code: str) -> LoginResponse:
    # Get the authed user
    response = requests.post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET,
            "code": code,
        },
    )
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Slack API Error")

    if response.json()["ok"] is False:
        raise HTTPException(status_code=403, detail="Slack API Error")

    auth_response = SlackAuthResponse(**response.json())

    # Get the user info
    response = requests.get(
        "https://slack.com/api/openid.connect.userInfo",
        params={
            "user": auth_response.authed_user.id,
        },
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": f"Bearer {auth_response.authed_user.access_token}",
        },
    )
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Slack API Error")
    user_info = SlackOpenIdConnectUserInfo(**response.json())

    return LoginResponse(
        user=User(
            id=auth_response.authed_user.id,
            name=user_info.name,
            profile_picture=user_info.picture,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        ),
        token="token",
    )
