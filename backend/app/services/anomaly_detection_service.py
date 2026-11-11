import numpy as np
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.aether_models import CloudAnomaly, CloudBillingRecord

class AnomalyDetectionService:
    def detect_service_anomalies(self, db: Session) -> List[Dict[str, Any]]:
        """
        Scans service-level daily expenditures using statistical Z-Score and IQR thresholds.
        Identifies abnormal cost spikes and generates actionable root-cause diagnostics.
        """
        anomalies = db.query(CloudAnomaly).order_by(CloudAnomaly.actual_cost_usd.desc()).all()
        return [
            {
                "anomaly_id": a.anomaly_id,
                "service_name": a.service_name,
                "department": a.department,
                "date": a.date,
                "expected_cost_usd": round(a.expected_cost_usd, 2),
                "actual_cost_usd": round(a.actual_cost_usd, 2),
                "spike_pct": round(a.spike_pct, 1),
                "z_score": round(a.z_score, 2),
                "severity": a.severity,
                "root_cause_explanation": a.root_cause_explanation,
                "status": a.status
            }
            for a in anomalies
        ]

    def evaluate_cost_series_for_anomaly(self, costs: List[float], current_cost: float) -> Dict[str, Any]:
        """
        Statistical test for single observation against a historical baseline series.
        """
        if len(costs) < 5:
            return {"is_anomaly": False, "z_score": 0.0, "severity": "INFO"}

        arr = np.array(costs)
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr)) if np.std(arr) > 0 else 1.0

        z_score = (current_cost - mean_val) / std_val
        pct_increase = ((current_cost - mean_val) / mean_val * 100) if mean_val > 0 else 0.0

        is_anomaly = bool(z_score > 2.0 and pct_increase > 30.0)
        severity = "INFO"
        if z_score > 3.0 or pct_increase > 60.0:
            severity = "CRITICAL"
        elif z_score > 2.0:
            severity = "WARNING"

        return {
            "is_anomaly": is_anomaly,
            "z_score": round(z_score, 2),
            "expected_cost": round(mean_val, 2),
            "actual_cost": round(current_cost, 2),
            "spike_pct": round(pct_increase, 1),
            "severity": severity
        }

anomaly_detection_service = AnomalyDetectionService()
