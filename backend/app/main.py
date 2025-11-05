from fastapi import FastAPI
from app.routers import auth, holdings
from app.database import engine
from app.models import user, asset, holding

app = FastAPI(
    title="Investment Holdings API",
    description="A simple FastAPI backend for tracking investment holdings with JWT authentication",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(holdings.router, prefix="/holdings", tags=["holdings"])

@app.get("/")
async def root():
    return {"message": "Investment Holdings API", "version": "1.0.0"}