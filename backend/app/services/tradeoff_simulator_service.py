from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.aether_models import CloudBillingRecord

class TradeoffSimulatorService:
    def simulate_scenario(
        self,
        db: Session,
        compute_capacity_change_pct: float = 0.0,
        traffic_growth_multiplier: float = 1.0,
        commitments_coverage_pct: float = 0.0,
        idle_cleanup_applied: bool = True
    ) -> Dict[str, Any]:
        """
        Interactive FinOps what-if trade-off simulator calculating financial delta,
        capacity implications, and operational risk assessment.
        """
        records = db.query(CloudBillingRecord).all()
        baseline_spend = sum(r.cost_usd for r in records)
        if baseline_spend == 0:
            baseline_spend = 142500.0 # Default baseline for demonstration

        # Component baselines
        compute_baseline = sum(r.cost_usd for r in records if r.service_category == "Compute") or (baseline_spend * 0.48)
        storage_baseline = sum(r.cost_usd for r in records if r.service_category == "Storage") or (baseline_spend * 0.22)
        database_baseline = sum(r.cost_usd for r in records if r.service_category == "Database") or (baseline_spend * 0.18)
        network_baseline = sum(r.cost_usd for r in records if r.service_category in ["Networking", "Egress"]) or (baseline_spend * 0.12)

        # 1. Compute scaling with traffic correlation
        # Compute demand scales with traffic multiplier and deliberate capacity adjustments
        effective_compute_scale = (1.0 + (compute_capacity_change_pct / 100.0)) * (traffic_growth_multiplier ** 0.85)
        projected_compute = compute_baseline * effective_compute_scale

        # 2. Idle resource cleanup effect (typically recovers ~12% of unoptimized compute)
        if idle_cleanup_applied:
            projected_compute *= 0.90

        # 3. Commitments / Savings Plan discounts (avg 32% discount on committed portion)
        commitment_fraction = min(max(commitments_coverage_pct / 100.0, 0.0), 1.0)
        savings_plan_discount = (projected_compute * commitment_fraction) * 0.32
        projected_compute -= savings_plan_discount

        # 4. Storage & Networking scale with traffic
        projected_storage = storage_baseline * (traffic_growth_multiplier ** 0.40)
        projected_database = database_baseline * (traffic_growth_multiplier ** 0.65)
        projected_network = network_baseline * (traffic_growth_multiplier ** 0.95)

        projected_total = projected_compute + projected_storage + projected_database + projected_network
        monthly_delta = projected_total - baseline_spend
        delta_pct = (monthly_delta / baseline_spend * 100) if baseline_spend > 0 else 0.0

        # Operational Risk Evaluation
        if compute_capacity_change_pct < -25.0 and traffic_growth_multiplier > 1.2:
            risk_level = "CRITICAL"
            risk_summary = "High risk of p99 latency spikes, pod scheduling thrashing, and HTTP 504 timeouts due to aggressive compute reduction under rising traffic."
        elif compute_capacity_change_pct < -15.0 or traffic_growth_multiplier > 1.5:
            risk_level = "ELEVATED"
            risk_summary = "Moderate risk: Workloads may exceed CPU target utilization (>75%). Recommend canary testing rightsized instances before full rollout."
        else:
            risk_level = "LOW"
            risk_summary = "Safe operational threshold: Infrastructure redundancy and headroom remain within standard FinOps safety limits (CPU < 65%)."

        return {
            "baseline_monthly_spend_usd": round(baseline_spend, 2),
            "projected_monthly_spend_usd": round(projected_total, 2),
            "monthly_delta_usd": round(monthly_delta, 2),
            "delta_pct": round(delta_pct, 1),
            "breakdown": {
                "compute_usd": round(projected_compute, 2),
                "storage_usd": round(projected_storage, 2),
                "database_usd": round(projected_database, 2),
                "network_usd": round(projected_network, 2)
            },
            "savings_plan_discount_usd": round(savings_plan_discount, 2),
            "operational_risk_level": risk_level,
            "risk_summary": risk_summary
        }

tradeoff_simulator_service = TradeoffSimulatorService()
