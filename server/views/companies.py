from typing import List

from db.company import (
    create_company,
    delete_my_company,
    edit_company,
    get_all_companies,
    get_companies_by_user_id,
    get_company_by_id,
)
from db.job_posting import get_job_postings_by_company_id
from db.user import get_logged_in_user
from fastapi import APIRouter, Depends, HTTPException
from models import Company, JobPosting

router = APIRouter()


@router.get("/companies", tags=["public"])
async def get_companies() -> List[Company]:
    return get_all_companies()


@router.post("/company", tags=["authentication required"])
async def post_company(company: Company, user=Depends(get_logged_in_user)) -> Company:
    return create_company(company, user)


@router.put("/company/{company_id}", tags=["authentication required"])
async def put_company(company_id: str, company: Company, user=Depends(get_logged_in_user)) -> Company:
    if company_id != company.id:
        raise HTTPException(status_code=403, detail="Invalid Auth Token")
    return edit_company(company, user)


@router.delete("/company/{company_id}", tags=["authentication required"])
async def delete_company(company_id: str, user=Depends(get_logged_in_user)) -> None:
    company = get_company_by_id(company_id)
    is_valid = company.user_id == user.id or user.is_admin
    print(company.user_id == user.id, user.is_admin, is_valid)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Invalid Auth Token")
    return delete_my_company(company_id)


@router.get("/company/{company_id}", tags=["public"])
async def get_company(company_id: str) -> Company:
    return get_company_by_id(company_id)


@router.get("/company/{company_id}/postings", tags=["public"])
async def get_company_postings(company_id: str) -> List[JobPosting]:
    return get_job_postings_by_company_id(company_id)


@router.get("/user/{user_id}/companies", tags=["authentication required"])
async def get_my_companies(user_id: str, user=Depends(get_logged_in_user)) -> List[Company]:
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Invalid Auth Token")
    return get_companies_by_user_id(user_id)
