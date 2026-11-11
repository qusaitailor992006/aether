from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.anomaly_detection_service import anomaly_detection_service

router = APIRouter(prefix="/api/anomalies", tags=["Anomaly Detection"])

@router.get("")
def get_anomalies(db: Session = Depends(get_db)):
    return anomaly_detection_service.detect_service_anomalies(db)
