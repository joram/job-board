import datetime
from typing import List

import boto3
from db import get_logged_in_user
from examples import example_job_posting
from fastapi import APIRouter, Depends
from models import Company, JobPosting
from views.users import prefixed_uuid

router = APIRouter()


@router.post("/job_posting", tags=["authentication required"])
def post_job_posting(job_posting: JobPosting, user=Depends(get_logged_in_user)) -> JobPosting:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("jb-job_postings")
    uid = prefixed_uuid("job_posting_")
    item = {
        "id": {"S": uid},
        "user_id": {"S": user.id},
        "job_title": {"S": job_posting.job_title},
        "description": job_posting.description,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
    }
    if job_posting.company_id:
        item["company_id"] = {"S": job_posting.company_id}

    response = table.put_item(Item=item)

    job_posting.id = uid
    job_posting.created_at = datetime.datetime.now()
    job_posting.updated_at = datetime.datetime.now()
    return job_posting


@router.get("/posting/{posting_id}", tags=["public"])
def get_posting(posting_id: str) -> JobPosting:
    return example_job_posting


@router.get("/postings", tags=["public"])
def get_postings() -> List[JobPosting]:
    # TODO: implement pagination
    # TODO: implement filtering
    return [example_job_posting, example_job_posting, example_job_posting, example_job_posting]
