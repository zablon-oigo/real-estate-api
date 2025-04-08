from fastapi import FastAPI

app=FastAPI(
    title="Real Estate API",
    description="Property listing API",
    version="1.0"
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


