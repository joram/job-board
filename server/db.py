import datetime

import boto3
from fastapi import Header, HTTPException
from models import Company, JobPosting, User
from pydantic.class_validators import List
from views.users import prefixed_uuid

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
        TableName="jb-users", KeyConditionExpression="id = :id", ExpressionAttributeValues={":id": {"S": user_id}}
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


def create_company(company: Company, user: User) -> Company:
    uid = prefixed_uuid("company_")
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
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
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
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
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    dynamodb.delete_item(
        TableName="jb-companies",
        Key={"id": {"S": company_id}},
    )
    return None


def get_companies_by_user_id(user_id: str) -> List[Company]:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
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


def get_job_postings_by_company_id(company_id: str) -> List[JobPosting]:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    response = dynamodb.scan(
        TableName="jb-job_postings",
        FilterExpression="company_id = :company_id",
        ExpressionAttributeValues={":company_id": {"S": company_id}},
    )
    job_postings = []
    for item in response["Items"]:
        job_posting = JobPosting(
            id=item["id"]["S"],
            company_id=item["company_id"]["S"],
            title=item["title"]["S"],
            description=item["description"]["S"],
            location=item["location"]["S"],
            salary=item["salary"]["S"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        job_postings.append(job_posting)
    return job_postings


def get_company_by_id(company_id: str) -> Company:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
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
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    response = dynamodb.scan(
        TableName="jb-companies",
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
            address=item.get("address", {}).get("S"),
        )
        companies.append(company)
    return companies
