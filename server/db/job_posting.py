import datetime
from typing import List

import boto3
from models import JobPosting


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
