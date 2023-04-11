import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from views.companies import router as company_router
from views.job_postings import router as job_posting_router
from views.users import router as user_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(company_router)
app.include_router(job_posting_router)


@app.get("/")
def get_root():
    return {"message": "FastAPI running in a Lambda function"}


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
