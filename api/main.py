from fastapi import FastAPI
from .routers import auth
app=FastAPI(
    title="Real Estate API",
    description="Property listing API",
    version="1.0"
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth.router)