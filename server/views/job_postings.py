from typing import List

from fastapi import APIRouter
from models import JobPosting

router = APIRouter()

example_job_posting = JobPosting(
    id="job_posting_id",
    user_id="user_id",
    company_id="company_id",
    job_title="Software Engineer",
    description="We are looking for a software engineer to join our team",
    benefits="Health benefits, 401k, etc.",
    application_url="https://www.google.com",
    min_salary=100000,
    max_salary=120000,
    salary_currency="CAD",
    created_at="2021-01-01T00:00:00Z",
    updated_at="2021-01-01T00:00:00Z",
)


@router.get("/posting/{posting_id}", tags=["public"])
def get_posting(posting_id: str) -> JobPosting:
    return example_job_posting


@router.get("/postings", tags=["public"])
def get_postings() -> List[JobPosting]:
    # TODO: implement pagination
    # TODO: implement filtering
    return [example_job_posting]
