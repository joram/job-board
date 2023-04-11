import datetime
from typing import Optional
from uuid import uuid4

import boto3
import requests
import settings
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    id: str
    profile_picture: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    access_token: Optional[str]


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


dynamodb = boto3.client("dynamodb", region_name="ca-central-1")


def prefixed_uuid(prefix: str) -> str:
    return prefix + str(uuid4())


def create_access_token(user: User) -> str:
    uuid = prefixed_uuid("access_token_")
    dynamodb.put_item(
        TableName="jb-auth_tokens",
        Item={
            "id": {"S": uuid},
            "token": {"S": uuid},
            "user_id": {"S": user.id},
            "created_at": {"S": datetime.datetime.now().isoformat()},
            "expires_at": {"S": (datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat()},
            "updated_at": {"S": datetime.datetime.now().isoformat()},
        },
    )
    return uuid


def get_or_create_user(name: str, slack_id: str, profile_picture: str) -> User:
    response = dynamodb.query(
        TableName="jb-users", KeyConditionExpression="id = :id", ExpressionAttributeValues={":id": {"S": slack_id}}
    )
    if len(response["Items"]) > 0:
        print("got existing user", response["Items"][0])
        return User(
            id=response["Items"][0]["id"]["S"],
            name=response["Items"][0]["name"]["S"],
            profile_picture=response["Items"][0]["profile_picture"]["S"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

    item = {
        "id": {"S": slack_id},
        "name": {"S": name},
        "profile_picture": {"S": profile_picture},
        "created_at": {"S": datetime.datetime.now().isoformat()},
        "updated_at": {"S": datetime.datetime.now().isoformat()},
    }
    dynamodb.put_item(
        TableName="jb-users",
        Item=item,
    )
    print("creating new user", item)

    return User(
        id=slack_id,
        name=name,
        profile_picture=profile_picture,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )


@router.get("/login", tags=["public"])
async def get_login(code: str) -> User:
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

    user = get_or_create_user(user_info.name, auth_response.authed_user.id, user_info.picture)
    access_token = create_access_token(user)
    user.access_token = access_token

    return user
