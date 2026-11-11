from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.aether_schemas import AIQueryRequest
from backend.app.services.ai_finops_service import ai_finops_service

router = APIRouter(prefix="/api/ai", tags=["AI FinOps Assistant"])

@router.post("/query")
def query_finops_assistant(req: AIQueryRequest, db: Session = Depends(get_db)):
    return ai_finops_service.answer_finops_query(db, req.query)
