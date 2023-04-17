import datetime

import boto3
import settings
from fastapi import Header, HTTPException
from models import User
from utils import prefixed_uuid

dynamodb = boto3.client("dynamodb", region_name="ca-central-1")


def get_or_create_user(name: str, email: str, profile_picture: str) -> User:
    response = dynamodb.query(
        TableName="jb-users", KeyConditionExpression="id = :id", ExpressionAttributeValues={":id": {"S": email}}
    )
    if len(response["Items"]) > 0:
        print("got existing user", response["Items"][0])
        return User(
            id=response["Items"][0]["id"]["S"],
            is_admin=email in settings.ADMIN_EMAILS,
            name=response["Items"][0]["name"]["S"],
            profile_picture=response["Items"][0]["profile_picture"]["S"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

    item = {
        "id": {"S": email},
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
        id=email,
        is_admin=email in settings.ADMIN_EMAILS,
        name=name,
        profile_picture=profile_picture,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )


def _get_logged_in_user(auth_token: str) -> User:
    if auth_token is None:
        print("No auth token provided")
        raise HTTPException(status_code=403, detail="Invalid Auth Token")

    response = dynamodb.query(
        TableName="jb-auth_tokens", KeyConditionExpression="id = :id", ExpressionAttributeValues={":id": {"S": auth_token}}
    )
    if len(response["Items"]) == 0:
        print("no token found")
        raise HTTPException(status_code=403, detail="Invalid Auth Token")

    token = response["Items"][0]
    user_id = token["user_id"]["S"]

    response = dynamodb.query(
        TableName="jb-users",
        KeyConditionExpression="id = :id",
        ExpressionAttributeValues={":id": {"S": user_id}},
    )
    if len(response["Items"]) == 0:
        print("no user found")
        raise HTTPException(status_code=403, detail="Invalid Auth Token")

    user = User(
        id=response["Items"][0]["id"]["S"],
        is_admin=response["Items"][0]["id"]["S"] in settings.ADMIN_EMAILS,
        name=response["Items"][0]["name"]["S"],
        profile_picture=response["Items"][0]["profile_picture"]["S"],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        data={},
    )
    return user


def get_logged_in_user(auth_token: str = Header(default=None, alias="X-Api-Key")) -> User:
    return _get_logged_in_user(auth_token)


def get_logged_in_admin_user(auth_token: str = Header(default=None, alias="X-Api-Key")) -> User:
    user = _get_logged_in_user(auth_token)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Invalid Auth Token")
    return user


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
