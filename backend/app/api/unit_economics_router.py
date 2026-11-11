from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.unit_economics_service import unit_economics_service

router = APIRouter(prefix="/api/unit-economics", tags=["Unit Economics"])

@router.get("")
def get_unit_economics(db: Session = Depends(get_db)):
    return unit_economics_service.get_unit_economics_metrics(db)
