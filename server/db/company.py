import datetime
from typing import List

import boto3
from fastapi import HTTPException
from models import Company, User
from utils import prefixed_uuid

dynamodb = boto3.client("dynamodb", region_name="ca-central-1")


def create_company(company: Company, user: User) -> Company:
    uid = prefixed_uuid("company_")
    dynamodb.put_item(
        TableName="jb-companies",
        Item={
            "id": {"S": uid},
            "user_id": {"S": user.id},
            "name": {"S": company.name},
            "description": {"S": company.description},
            "logo_url": {"S": company.logo_url},
            "website_url": {"S": company.website_url},
            "created_at": {"S": datetime.datetime.now().isoformat()},
            "updated_at": {"S": datetime.datetime.now().isoformat()},
        },
    )

    company.user_id = user.id
    company.id = uid
    company.created_at = datetime.datetime.now().isoformat()
    company.updated_at = datetime.datetime.now().isoformat()
    return company


def edit_company(company: Company, user: User) -> Company:
    dynamodb.update_item(
        TableName="jb-companies",
        Key={"id": {"S": company.id}},
        AttributeUpdates={
            "user_id": {"Value": {"S": user.id}},
            "name": {"Value": {"S": company.name}},
            "description": {"Value": {"S": company.description}},
            "logo_url": {"Value": {"S": company.logo_url}},
            "website_url": {"Value": {"S": company.website_url}},
            "updated_at": {"Value": {"S": datetime.datetime.now().isoformat()}},
            "address": {"Value": {"S": company.address}},
        },
    )

    company.updated_at = datetime.datetime.now().isoformat()
    return company


def delete_my_company(company_id: str) -> None:
    dynamodb.delete_item(
        TableName="jb-companies",
        Key={"id": {"S": company_id}},
    )
    return None


def get_company_by_id(company_id: str) -> Company:
    response = dynamodb.scan(
        TableName="jb-companies", FilterExpression="id = :id", ExpressionAttributeValues={":id": {"S": company_id}}
    )
    if len(response["Items"]) == 0:
        raise HTTPException(status_code=404, detail="Company not found")

    item = response["Items"][0]
    company = Company(
        id=item["id"]["S"],
        user_id=item["user_id"]["S"],
        name=item["name"]["S"],
        description=item["description"]["S"],
        logo_url=item["logo_url"]["S"],
        website_url=item["website_url"]["S"],
        address=item.get("address", {}).get("S"),
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    return company


def get_all_companies() -> List[Company]:
    response = dynamodb.scan(TableName="jb-companies")
    companies = []
    for item in response["Items"]:
        company = Company(
            id=item["id"]["S"],
            user_id=item["user_id"]["S"],
            name=item["name"]["S"],
            description=item["description"]["S"],
            logo_url=item["logo_url"]["S"],
            website_url=item["website_url"]["S"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            address=item.get("address", {}).get("S"),
        )
        companies.append(company)
    return companies


def get_companies_by_user_id(user_id: str) -> List[Company]:
    response = dynamodb.scan(
        TableName="jb-companies", FilterExpression="user_id = :user_id", ExpressionAttributeValues={":user_id": {"S": user_id}}
    )
    companies = []
    for item in response["Items"]:
        company = Company(
            id=item["id"]["S"],
            user_id=item["user_id"]["S"],
            name=item["name"]["S"],
            description=item["description"]["S"],
            logo_url=item["logo_url"]["S"],
            website_url=item["website_url"]["S"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        companies.append(company)
    return companies
