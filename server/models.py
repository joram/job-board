import datetime
import enum
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel


class Currency(enum.Enum):
    CAD = "CAD"
    USD = "USD"


class BaseModel(PydanticBaseModel):
    id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    data: dict


class AuthToken(BaseModel):
    user_id: str

    token: str
    expires_at: datetime.datetime


class Company(BaseModel):
    user_id: str

    name: str
    description: str
    logo_url: str
    website_url: str
    address: Optional[str]


class JobPosting(BaseModel):
    user_id: str
    company: Optional[Company]
    company_id: Optional[str]

    job_title: str
    description: str
    benefits: str
    application_url: str
    min_salary: int
    max_salary: int
    salary_currency: Currency
