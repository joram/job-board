from models import AuthToken as ModelAuthToken
from models import Company as ModelCompany
from models import JobPosting as ModelJobPosting
from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class User(Model):
    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

    name = UnicodeAttribute()
    description = UnicodeAttribute()
    logo_url = UnicodeAttribute()
    website_url = UnicodeAttribute()

    class Meta:
        table_name = "jb-users"
        region = "us-east-1"


class AuthToken(Model):
    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()
    expires_at = UTCDateTimeAttribute()

    user_id = UnicodeAttribute()
    token = UnicodeAttribute()

    def to_model(self):
        return ModelAuthToken(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            expires_at=self.expires_at,
            user_id=self.user_id,
            token=self.token,
        )

    class Meta:
        table_name = "jb-auth_tokens"
        region = "us-east-1"


class JobPosting(Model):
    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()
    user_id = UnicodeAttribute()
    company_id = UnicodeAttribute()

    job_title = UnicodeAttribute()
    description = UnicodeAttribute()
    benefits = UnicodeAttribute()
    application_url = UnicodeAttribute()
    min_salary = NumberAttribute()
    max_salary = NumberAttribute()
    salary_currency = UnicodeAttribute()

    def to_model(self):
        return ModelJobPosting(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            company_id=self.company_id,
            job_title=self.job_title,
            description=self.description,
            benefits=self.benefits,
            application_url=self.application_url,
            min_salary=self.min_salary,
            max_salary=self.max_salary,
            salary_currency=self.salary_currency,
        )

    class Meta:
        table_name = "jb-job_postings"
        region = "us-east-1"


class Company(Model):
    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()
    user_id = UnicodeAttribute()

    name = UnicodeAttribute()
    description = UnicodeAttribute()
    logo_url = UnicodeAttribute()
    website_url = UnicodeAttribute()

    def to_model(self):
        return ModelCompany(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            name=self.name,
            description=self.description,
            logo_url=self.logo_url,
            website_url=self.website_url,
        )

    class Meta:
        table_name = "jb-companies"
        region = "us-east-1"
