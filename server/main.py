from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def get_root():
    return {"message": "FastAPI running in a Lambda function"}


@app.get("/company")
def get_company():
    return {"message": "FastAPI running in a Lambda function"}


@app.get("/posting")
def get_posting():
    return {"message": "FastAPI running in a Lambda function"}


handler = Mangum(app)
