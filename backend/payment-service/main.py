import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import payment_routes
from app.database.models.payment_model import Payment

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[Payment]
    )
    print("🚀 Connected to MongoDB Atlas and initialized Beanie")
    yield
    client.close()
    print("🛑 MongoDB connection closed")

app = FastAPI(title="Bakong Payment Microservice", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://e-commerce-testing-tan.vercel.app",
        "https://e-smart-shop.vercel.app",
        "https://backend-1-lcio.onrender.com/api/v1/orders",
        "https://backend-1-lcio.onrender.com/api",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_routes.router, prefix="/api/v1/payments")

@app.get("/health")
async def health_check():
    return "ok"

@app.get("/")
async def root():
    return {"message": "Payment Service is Online"}

# Only use this for local dev
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port)
    
    
