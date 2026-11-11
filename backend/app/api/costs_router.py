from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.services.cost_intelligence_service import cost_intelligence_service
from backend.app.services.billing_ingestion_service import billing_ingestion_service
from backend.app.schemas.aether_schemas import CostOverviewResponse

router = APIRouter(prefix="/api/costs", tags=["Cost Intelligence"])

@router.get("/overview")
def get_cost_overview(days: int = 30, db: Session = Depends(get_db)):
    return cost_intelligence_service.get_cost_overview(db, days=days)

@router.post("/ingest")
def ingest_billing_records(records: List[Dict[str, Any]], db: Session = Depends(get_db)):
    count = billing_ingestion_service.normalize_and_ingest_records(db, records)
    return {"message": f"Successfully ingested and normalized {count} billing records.", "count": count}
