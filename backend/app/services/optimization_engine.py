import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.aether_models import OptimizationRecommendation, FinOpsAuditLog

class OptimizationEngine:
    def get_recommendations(self, db: Session) -> Dict[str, Any]:
        """
        Retrieves all FinOps optimization recommendations, categorizing by type
        and computing total potential monthly cost savings.
        """
        recs = db.query(OptimizationRecommendation).all()
        
        total_potential_savings = sum(r.estimated_monthly_savings_usd for r in recs if r.human_approval_status != "DISMISSED")
        approved_savings = sum(r.estimated_monthly_savings_usd for r in recs if r.human_approval_status == "APPROVED")

        recommendations_list = [
            {
                "recommendation_id": r.recommendation_id,
                "resource_id": r.resource_id,
                "service_name": r.service_name,
                "department": r.department,
                "optimization_type": r.optimization_type,
                "current_monthly_cost_usd": round(r.current_monthly_cost_usd, 2),
                "estimated_monthly_savings_usd": round(r.estimated_monthly_savings_usd, 2),
                "effort": r.effort,
                "confidence_score": round(r.confidence_score, 2),
                "justification": r.justification,
                "human_approval_status": r.human_approval_status
            }
            for r in recs
        ]

        return {
            "total_potential_savings_usd": round(total_potential_savings, 2),
            "approved_savings_usd": round(approved_savings, 2),
            "pending_count": sum(1 for r in recs if r.human_approval_status == "PENDING_APPROVAL"),
            "recommendations": recommendations_list
        }

    def update_approval_status(self, db: Session, recommendation_id: str, new_status: str, user_email: str = "finops-lead@enterprise.com") -> Dict[str, Any]:
        """
        Updates human review approval state and logs action into the FinOps audit trail.
        """
        rec = db.query(OptimizationRecommendation).filter(OptimizationRecommendation.recommendation_id == recommendation_id).first()
        if not rec:
            return {"error": "Recommendation not found", "success": False}

        old_status = rec.human_approval_status
        rec.human_approval_status = new_status
        
        # Log to Audit Table
        audit = FinOpsAuditLog(
            id=str(uuid.uuid4()),
            action=f"RECOMMENDATION_{new_status.upper()}",
            entity_type="OptimizationRecommendation",
            entity_id=rec.recommendation_id,
            user_email=user_email,
            details=f"Status changed from {old_status} to {new_status} for resource {rec.resource_id} (Est. savings: ${rec.estimated_monthly_savings_usd}/mo)"
        )
        db.add(audit)
        db.commit()

        return {
            "success": True,
            "recommendation_id": rec.recommendation_id,
            "new_status": rec.human_approval_status,
            "estimated_savings_usd": rec.estimated_monthly_savings_usd
        }

optimization_engine = OptimizationEngine()
