from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.aether_models import DepartmentBudget

router = APIRouter(prefix="/api/budgets", tags=["Budget Management"])

@router.get("")
def get_department_budgets(db: Session = Depends(get_db)):
    budgets = db.query(DepartmentBudget).all()
    return [
        {
            "department": b.department,
            "monthly_budget_usd": round(b.monthly_budget_usd, 2),
            "current_spend_usd": round(b.current_spend_usd, 2),
            "forecasted_spend_usd": round(b.forecasted_spend_usd, 2),
            "variance_pct": round(b.variance_pct, 1),
            "status": b.status,
            "month": b.month
        }
        for b in budgets
    ]
