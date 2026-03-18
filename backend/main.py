from dotenv import load_dotenv
load_dotenv()  # must be first

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router

# Ensure required env variables exist
if not os.getenv("DATABASE_URL"):
    raise ValueError("DATABASE_URL not set")
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not set")

# Initialize FastAPI
app = FastAPI(title="CRM Marketing & Sales Assistant")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Health check
@app.get("/")
def root():
    return {"status": "CRM Assistant API Running"}