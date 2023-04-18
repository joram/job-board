from typing import List

from db.job_posting import (
    create_job_posting,
    get_all_postings,
    get_job_posting_by_posting_id,
    remove_job_posting,
    update_job_posting,
)
from db.user import get_logged_in_user
from examples import example_job_posting
from fastapi import APIRouter, Depends, HTTPException
from models import JobPosting

router = APIRouter()


@router.post("/job_posting", tags=["authentication required"])
def post_job_posting(job_posting: JobPosting, user=Depends(get_logged_in_user)) -> JobPosting:
    return create_job_posting(job_posting, user)


@router.patch("/job_posting/{posting_id}", tags=["authentication required"])
def patch_job_posting(posting_id: str, job_posting: JobPosting, user=Depends(get_logged_in_user)) -> JobPosting:
    job_posting = get_job_posting_by_posting_id(posting_id)
    if job_posting.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this job posting")

    return update_job_posting(job_posting, user)


@router.get("/posting/{posting_id}", tags=["public"])
def get_posting(posting_id: str) -> JobPosting:
    return get_job_posting_by_posting_id(posting_id)


@router.delete("/job_posting/{posting_id}", tags=["authentication required"])
def delete_job_posting(posting_id: str, user=Depends(get_logged_in_user)):
    job_posting = get_job_posting_by_posting_id(posting_id)
    if job_posting.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this job posting")

    remove_job_posting(posting_id)


@router.get("/user/{user_id}/postings", tags=["authentication required"])
def get_my_postings(user_id: str, user=Depends(get_logged_in_user)) -> List[JobPosting]:
    return [example_job_posting]


@router.get("/postings", tags=["public"])
def get_postings() -> List[JobPosting]:
    return get_all_postings()
