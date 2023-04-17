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
    profile_picture: str
    access_token: Optional[str]
    is_admin: Optional[bool]


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


class AuthedUser(BaseModel):
    id: str
    scope: str
    access_token: str
    token_type: str


class Team(BaseModel):
    id: str


class SlackAuthResponse(BaseModel):
    ok: bool
    app_id: str
    authed_user: AuthedUser
    team: Team
    enterprise: Optional[str]
    is_enterprise_install: bool


class SlackOpenIdConnectUserInfo(BaseModel):
    ok: bool
    name: str
    picture: str
