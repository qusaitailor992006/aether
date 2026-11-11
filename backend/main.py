import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.models.aether_models import *
from backend.app.services.synthetic_billing_generator import synthetic_billing_generator
from backend.app.api.costs_router import router as costs_router
from backend.app.api.budgets_router import router as budgets_router
from backend.app.api.anomalies_router import router as anomalies_router
from backend.app.api.optimizations_router import router as optimizations_router
from backend.app.api.unit_economics_router import router as unit_economics_router
from backend.app.api.simulator_router import router as simulator_router
from backend.app.api.ai_router import router as ai_router

# Initialize Database Schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Cloud FinOps & Infrastructure Economics Intelligence Platform.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(costs_router)
app.include_router(budgets_router)
app.include_router(anomalies_router)
app.include_router(optimizations_router)
app.include_router(unit_economics_router)
app.include_router(simulator_router)
app.include_router(ai_router)

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        synthetic_billing_generator.seed_initial_enterprise_data(db)
    finally:
        db.close()

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "platform": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.PORT, reload=True)
