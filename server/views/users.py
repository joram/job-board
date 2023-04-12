import requests
import settings
from db.user import create_access_token, get_or_create_user
from fastapi import APIRouter, HTTPException
from models import SlackAuthResponse, SlackOpenIdConnectUserInfo, User

router = APIRouter()


def get_slack_auth_response(code: str) -> SlackAuthResponse:
    response = requests.post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET,
            "code": code,
        },
    )
    if response.status_code != 200:
        print(response.text)
        raise HTTPException(status_code=403, detail="1: " + response.text)

    if response.json()["ok"] is False:
        print(response.text)
        raise HTTPException(status_code=403, detail="2: " + response.text)

    auth_response = SlackAuthResponse(**response.json())
    return auth_response


def get_slack_user_info(auth_response: SlackAuthResponse) -> SlackOpenIdConnectUserInfo:
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
        print(response.text)
        raise HTTPException(status_code=403, detail=response.text)
    user_info = SlackOpenIdConnectUserInfo(**response.json())
    return user_info


@router.get("/login", tags=["public"])
async def get_login(code: str) -> User:
    auth_response = get_slack_auth_response(code)
    user_info = get_slack_user_info(auth_response)
    user = get_or_create_user(user_info.name, auth_response.authed_user.id, user_info.picture)
    access_token = create_access_token(user)
    user.access_token = access_token
    return user
