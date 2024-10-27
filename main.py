from fastapi import FastAPI
from app.routes import router as blog_router

app = FastAPI()

app.include_router(blog_router, prefix="/blogs", tags=["Blogs"])

@app.get("/")
async def root():
    return {"message": "Welcome to the School Blog API!"}
