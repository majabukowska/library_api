from fastapi import FastAPI

app = FastAPI(title="Library API")


@app.get("/")
def root():
    return {"message": "Library API is running"}