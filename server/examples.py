from models import Company, JobPosting

example_job_posting = JobPosting(
    id="job_posting_id",
    user_id="user_id",
    company=Company(
        id="company_id",
        user_id="user_id",
        name="Company Name",
        description="We are a company",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg",
        website_url="https://www.google.com",
        created_at="2021-01-01T00:00:00Z",
        updated_at="2021-01-01T00:00:00Z",
        address="",
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

example_company = Company(
    id="company_id",
    user_id="user_id",
    name="Company Name",
    description="We are a company",
    logo_url="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg",
    website_url="https://www.google.com",
    created_at="2021-01-01T00:00:00Z",
    updated_at="2021-01-01T00:00:00Z",
    address="",
)
