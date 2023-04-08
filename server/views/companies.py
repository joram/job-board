from typing import List

from db.models import Company as DBCompany
from db.models import JobPosting as DBJobPosting
from fastapi import APIRouter
from lib.fastapi import Depends
from models import Company, JobPosting
from utils import verify_auth_token

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

example_company = Company(
    id="company_id",
    user_id="user_id",
    name="Company Name",
    description="We are a company",
    logo_url="https://www.google.com",
    website_url="https://www.google.com",
    created_at="2021-01-01T00:00:00Z",
    updated_at="2021-01-01T00:00:00Z",
)


@router.get("/companies", tags=["public"])
async def get_companies() -> List[Company]:
    return [example_company]


@router.post("/company", tags=["authentication required"])
async def post_company() -> Company:
    return example_company


@router.post("/company/{company_id}", tags=["authentication required"])
async def post_update_company(company_id) -> Company:
    return example_company


@router.get("/company/{company_id}", tags=["public"])
async def get_company(company_id: str) -> Company:
    db_company = DBCompany.get(company_id)

    return db_company.to_model()


@router.get("/company/{company_id}/postings", tags=["public"])
async def get_company_postings(company_id: str) -> List[JobPosting]:
    # postings = DBJobPosting.query(company_id)

    return [example_job_posting]


@router.get("/user/{user_id}/companies", tags=["authentication required"])
async def get_companies(user_id: str, auth_token=Depends(verify_auth_token)) -> List[Company]:
    return [example_company]
