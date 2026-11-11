from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.aether_models import UnitEconomicsMetric

class UnitEconomicsService:
    def get_unit_economics_metrics(self, db: Session) -> Dict[str, Any]:
        """
        Retrieves enterprise unit economics, efficiency trends, and financial ratios.
        """
        metrics = db.query(UnitEconomicsMetric).order_by(UnitEconomicsMetric.date.asc()).all()
        if not metrics:
            return {
                "latest_metric": {},
                "historical_trend": [],
                "summary": "No unit economics data available."
            }

        history = [
            {
                "date": m.date,
                "active_customers": m.active_customers,
                "monthly_transactions": m.monthly_transactions,
                "api_requests_millions": round(m.api_requests_millions, 1),
                "monthly_revenue_usd": round(m.monthly_revenue_usd, 2),
                "total_cloud_spend_usd": round(m.total_cloud_spend_usd, 2),
                "cost_per_customer_usd": round(m.cost_per_customer_usd, 3),
                "cost_per_transaction_usd": round(m.cost_per_transaction_usd, 4),
                "cost_per_million_api_requests_usd": round(m.cost_per_million_api_requests_usd, 2),
                "cloud_spend_pct_of_revenue": round(m.cloud_spend_pct_of_revenue, 2)
            }
            for m in metrics
        ]

        latest = history[-1]
        first = history[0]
        
        # Calculate economies of scale efficiency improvement
        cust_cost_change_pct = ((latest["cost_per_customer_usd"] - first["cost_per_customer_usd"]) / first["cost_per_customer_usd"] * 100) if first["cost_per_customer_usd"] > 0 else 0.0
        txn_cost_change_pct = ((latest["cost_per_transaction_usd"] - first["cost_per_transaction_usd"]) / first["cost_per_transaction_usd"] * 100) if first["cost_per_transaction_usd"] > 0 else 0.0

        return {
            "latest": latest,
            "history": history,
            "economies_of_scale": {
                "cost_per_customer_change_pct": round(cust_cost_change_pct, 1),
                "cost_per_transaction_change_pct": round(txn_cost_change_pct, 1),
                "is_efficient_scaling": bool(cust_cost_change_pct < 0)
            }
        }

unit_economics_service = UnitEconomicsService()
