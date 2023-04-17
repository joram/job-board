import urllib.parse

import requests
import settings
from db.user import create_access_token, get_or_create_user
from fastapi import APIRouter, HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from models import SlackAuthResponse, SlackOpenIdConnectUserInfo
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

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


class GoogleJWT(BaseModel):
    aud: str
    azp: str
    email: str
    email_verified: bool
    exp: int
    family_name: str
    given_name: str
    iat: int
    iss: str
    jti: str
    name: str
    nbf: int
    picture: str
    sub: str


async def request_to_google_jwt(request: Request) -> GoogleJWT:
    data = (await request.body()).decode("utf-8")
    data = urllib.parse.parse_qs(data)
    idinfo = id_token.verify_oauth2_token(data["credential"][0], google_requests.Request(), settings.GOOGLE_CLIENT_ID)
    return GoogleJWT(**idinfo)


@router.post("/auth/google", tags=["public"])
async def post_auth_google(request: Request):
    google_jwt = await request_to_google_jwt(request)
    user = get_or_create_user(google_jwt.name, google_jwt.email, google_jwt.picture)
    user.access_token = create_access_token(user)
    get_params = urllib.parse.urlencode(dict(user))

    return RedirectResponse("https://localhost:3000/login?" + get_params, status_code=status.HTTP_302_FOUND)


# @router.get("/auth/slack", tags=["public"])
# async def get_login(code: str) -> User:
#     auth_response = get_slack_auth_response(code)
#     user_info = get_slack_user_info(auth_response)
#     user = get_or_create_user(user_info.name, auth_response.authed_user.id, user_info.picture)
#     access_token = create_access_token(user)
#     user.access_token = access_token
#     return user
