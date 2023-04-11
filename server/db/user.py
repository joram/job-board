import datetime

import boto3
from fastapi import Header, HTTPException
from models import User

dynamodb = boto3.client("dynamodb", region_name="ca-central-1")


def get_logged_in_user(auth_token: str = Header(default=None)) -> User:
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
        name=response["Items"][0]["name"]["S"],
        profile_picture=response["Items"][0]["profile_picture"]["S"],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        data={},
    )
    return user
