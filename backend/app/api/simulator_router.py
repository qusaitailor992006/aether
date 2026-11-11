from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.aether_schemas import ScenarioSimRequest
from backend.app.services.tradeoff_simulator_service import tradeoff_simulator_service

router = APIRouter(prefix="/api/simulator", tags=["Trade-off Simulator"])

@router.post("/tradeoff")
def run_tradeoff_simulation(req: ScenarioSimRequest, db: Session = Depends(get_db)):
    return tradeoff_simulator_service.simulate_scenario(
        db=db,
        compute_capacity_change_pct=req.compute_capacity_change_pct,
        traffic_growth_multiplier=req.traffic_growth_multiplier,
        commitments_coverage_pct=req.commitments_coverage_pct,
        idle_cleanup_applied=req.idle_cleanup_applied
    )
