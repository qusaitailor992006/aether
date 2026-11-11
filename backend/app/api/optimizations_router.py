from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.optimization_engine import optimization_engine

router = APIRouter(prefix="/api/optimizations", tags=["Resource Optimization"])

@router.get("")
def get_optimizations(db: Session = Depends(get_db)):
    return optimization_engine.get_recommendations(db)

@router.post("/{recommendation_id}/approve")
def approve_optimization(recommendation_id: str, db: Session = Depends(get_db)):
    return optimization_engine.update_approval_status(db, recommendation_id, "APPROVED")

@router.post("/{recommendation_id}/dismiss")
def dismiss_optimization(recommendation_id: str, db: Session = Depends(get_db)):
    return optimization_engine.update_approval_status(db, recommendation_id, "DISMISSED")
