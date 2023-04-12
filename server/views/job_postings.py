from typing import List

from db.job_posting import create_job_posting
from db.user import get_logged_in_user
from examples import example_job_posting
from fastapi import APIRouter, Depends
from models import JobPosting

router = APIRouter()


@router.post("/job_posting", tags=["authentication required"])
def post_job_posting(job_posting: JobPosting, user=Depends(get_logged_in_user)) -> JobPosting:
    return create_job_posting(job_posting, user)


@router.get("/posting/{posting_id}", tags=["public"])
def get_posting(posting_id: str) -> JobPosting:
    return example_job_posting


@router.get("/user/{user_id}/postings", tags=["authentication required"])
def get_my_postings(user_id: str, user=Depends(get_logged_in_user)) -> List[JobPosting]:
    return [example_job_posting]


@router.get("/postings", tags=["public"])
def get_postings() -> List[JobPosting]:
    # TODO: implement pagination
    # TODO: implement filtering
    return [example_job_posting, example_job_posting, example_job_posting, example_job_posting]
