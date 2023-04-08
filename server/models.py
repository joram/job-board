import datetime
import enum
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel


class Currency(enum.Enum):
    CAD = "CAD"
    USD = "USD"


class BaseModel(PydanticBaseModel):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    data: dict


class AuthToken(BaseModel):
    user_id: str

    token: str
    expires_at: datetime.datetime


class JobPosting(BaseModel):
    user_id: str
    company_id: Optional[str]

    job_title: str
    description: str
    benefits: str
    application_url: str
    min_salary: int
    max_salary: int
    salary_currency: Currency


class Company(BaseModel):
    user_id: str

    name: str
    description: str
    logo_url: str
    website_url: str
