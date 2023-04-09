from typing import List

from fastapi import APIRouter
from models import Company, JobPosting

router = APIRouter()

example_job_posting = JobPosting(
    id="job_posting_id",
    user_id="user_id",
    company=Company(
        id="company_id",
        user_id="user_id",
        name="Google",
        description="We are a tech company",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg",
        website_url="https://www.google.com",
        created_at="2021-01-01T00:00:00Z",
        updated_at="2021-01-01T00:00:00Z",
    ),
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
    return [example_job_posting, example_job_posting, example_job_posting, example_job_posting]
