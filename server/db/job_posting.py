import datetime
from typing import List

import boto3
from db.company import get_company_by_id
from fastapi import HTTPException
from models import JobPosting, User
from utils import prefixed_uuid


def get_job_posting_by_posting_id(posting_id: str) -> JobPosting:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    response = dynamodb.scan(
        TableName="jb-job_postings",
        FilterExpression="id = :posting_id",
        ExpressionAttributeValues={":posting_id": {"S": posting_id}},
    )
    if len(response["Items"]) == 0:
        raise HTTPException(status_code=404, detail="Company not found")

    item = response["Items"][0]

    job_posting = JobPosting(
        id=item["id"]["S"],
        company_id=item["company_id"]["S"],
        job_title=item["job_title"]["S"],
        description=item["description"]["S"],
        requirements=item["requirements"]["S"],
        benefits=item["benefits"]["S"],
        min_salary=item["min_salary"]["N"],
        max_salary=item["max_salary"]["N"],
        salary_currency=item["salary_currency"]["S"],
        user_id=item["user_id"]["S"],
        application_url=item["application_url"]["S"],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    if job_posting.company_id is not None:
        job_posting.company = get_company_by_id(job_posting.company_id)
    return job_posting


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


def create_job_posting(job_posting: JobPosting, user) -> JobPosting:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    uid = prefixed_uuid("job_posting_")
    item = {
        "id": {"S": uid},
        "user_id": {"S": user.id},
        "job_title": {"S": job_posting.job_title},
        "description": {"S": job_posting.description},
        "requirements": {"S": job_posting.requirements},
        "benefits": {"S": job_posting.benefits},
        "application_url": {"S": job_posting.application_url},
        "min_salary": {"N": str(job_posting.min_salary)},
        "max_salary": {"N": str(job_posting.max_salary)},
        "salary_currency": {"S": job_posting.salary_currency},
        "created_at": {"S": datetime.datetime.now().isoformat()},
        "updated_at": {"S": datetime.datetime.now().isoformat()},
    }
    if job_posting.company_id:
        item["company_id"] = {"S": job_posting.company_id}

    dynamodb.put_item(
        TableName="jb-job_postings",
        Item=item,
    )

    job_posting.id = uid
    job_posting.created_at = datetime.datetime.now()
    job_posting.updated_at = datetime.datetime.now()
    return job_posting


def update_job_posting(job_posting: JobPosting, user: User) -> JobPosting:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    dynamodb.update_item(
        TableName="jb-job_postings",
        Key={"id": {"S": job_posting.id}},
        AttributeUpdates={
            "user_id": {"Value": {"S": job_posting.user_id}},
            "job_title": {"Value": {"S": job_posting.job_title}},
            "description": {"Value": {"S": job_posting.description}},
            "requirements": {"Value": {"S": job_posting.requirements}},
            "benefits": {"Value": {"S": job_posting.benefits}},
            "application_url": {"Value": {"S": job_posting.application_url}},
            "min_salary": {"Value": {"N": str(job_posting.min_salary)}},
            "max_salary": {"Value": {"N": str(job_posting.max_salary)}},
            "salary_currency": {"Value": {"S": job_posting.salary_currency}},
            "created_at": {"Value": {"S": datetime.datetime.now().isoformat()}},
            "updated_at": {"Value": {"S": datetime.datetime.now().isoformat()}},
        },
    )
    return job_posting


def get_all_postings() -> List[JobPosting]:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    response = dynamodb.scan(TableName="jb-job_postings")
    job_postings = []
    for item in response["Items"]:
        job_posting = JobPosting(
            id=item["id"]["S"],
            company_id=item["company_id"]["S"],
            job_title=item["job_title"]["S"],
            description=item["description"]["S"],
            requirements=item["requirements"]["S"],
            benefits=item["benefits"]["S"],
            min_salary=item["min_salary"]["N"],
            max_salary=item["max_salary"]["N"],
            salary_currency=item["salary_currency"]["S"],
            user_id=item["user_id"]["S"],
            application_url=item["application_url"]["S"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        if job_posting.company_id is not None:
            job_posting.company = get_company_by_id(job_posting.company_id)
        job_postings.append(job_posting)
    return job_postings


def remove_job_posting(posting_id: str) -> None:
    dynamodb = boto3.client("dynamodb", region_name="ca-central-1")
    dynamodb.delete_item(
        TableName="jb-job_postings",
        Key={"id": {"S": posting_id}},
    )
    return None
