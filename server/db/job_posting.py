import datetime
from typing import List

import boto3
from models import JobPosting
from utils import prefixed_uuid


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
    dynamodb = boto3.resource("dynamodb", region_name="ca-central-1")
    table = dynamodb.Table("jb-job_postings")
    uid = prefixed_uuid("job_posting_")
    item = {
        "id": {"S": uid},
        "user_id": {"S": user.id},
        "company_id": {"S": job_posting.company_id},
        "job_title": {"S": job_posting.job_title},
        "description": job_posting.description,
        "benefits": job_posting.benefits,
        "application_url": job_posting.application_url,
        "min_salary": job_posting.min_salary,
        "max_salary": job_posting.max_salary,
        "salary_currency": job_posting.salary_currency,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
    }
    if job_posting.company_id:
        item["company_id"] = {"S": job_posting.company_id}

    table.put_item(Item=item)

    job_posting.id = uid
    job_posting.created_at = datetime.datetime.now()
    job_posting.updated_at = datetime.datetime.now()
    return job_posting
