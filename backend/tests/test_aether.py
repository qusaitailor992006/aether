import unittest
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.services.synthetic_billing_generator import synthetic_billing_generator
from backend.app.services.cost_intelligence_service import cost_intelligence_service
from backend.app.services.anomaly_detection_service import anomaly_detection_service
from backend.app.services.unit_economics_service import unit_economics_service
from backend.app.services.optimization_engine import optimization_engine
from backend.app.services.tradeoff_simulator_service import tradeoff_simulator_service

class TestAetherFinOps(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            synthetic_billing_generator.seed_initial_enterprise_data(db)
        finally:
            db.close()

    def test_cost_overview_and_forecasting(self):
        """Verify cost aggregation, category distribution, and forecasting."""
        db = SessionLocal()
        try:
            overview = cost_intelligence_service.get_cost_overview(db)
            self.assertGreater(overview["total_monthly_spend_usd"], 50000.0)
            self.assertGreater(overview["total_budget_usd"], 100000.0)
            self.assertIn("Compute", overview["spend_by_category"])
            self.assertIn("Engineering", overview["spend_by_department"])
            self.assertIn("GCP", overview["spend_by_provider"])
            self.assertGreater(len(overview["daily_spend_trend"]), 20)
            self.assertGreater(overview["forecasted_monthly_spend_usd"], 0)
        finally:
            db.close()

    def test_anomaly_detection_z_score(self):
        """Verify that statistical anomaly engine detects spikes and assigns severity."""
        db = SessionLocal()
        try:
            anomalies = anomaly_detection_service.detect_service_anomalies(db)
            self.assertGreater(len(anomalies), 0)
            top_anom = anomalies[0]
            self.assertIn(top_anom["severity"], ["CRITICAL", "WARNING"])
            self.assertGreater(top_anom["spike_pct"], 30.0)
            self.assertGreater(top_anom["z_score"], 2.0)
            self.assertTrue(len(top_anom["root_cause_explanation"]) > 10)
        finally:
            db.close()

    def test_unit_economics_calculations(self):
        """Verify unit costs: cost per customer, cost per transaction, and scaling efficiency."""
        db = SessionLocal()
        try:
            res = unit_economics_service.get_unit_economics_metrics(db)
            latest = res["latest"]
            self.assertGreater(latest["active_customers"], 50000)
            self.assertGreater(latest["monthly_transactions"], 500000)
            self.assertLess(latest["cost_per_customer_usd"], 3.50)
            self.assertLess(latest["cloud_spend_pct_of_revenue"], 15.0)
            self.assertTrue(res["economies_of_scale"]["is_efficient_scaling"])
        finally:
            db.close()

    def test_optimization_approval_workflow(self):
        """Verify human approval status updates and audit logging."""
        db = SessionLocal()
        try:
            opt_data = optimization_engine.get_recommendations(db)
            self.assertGreater(opt_data["total_potential_savings_usd"], 5000.0)
            self.assertGreater(len(opt_data["recommendations"]), 0)

            first_rec = opt_data["recommendations"][0]
            update_res = optimization_engine.update_approval_status(
                db, first_rec["recommendation_id"], "APPROVED", "finops-lead@enterprise.com"
            )
            self.assertTrue(update_res["success"])
            self.assertEqual(update_res["new_status"], "APPROVED")
        finally:
            db.close()

    def test_tradeoff_simulator_scenarios(self):
        """Verify interactive scenario simulation under compute reduction and traffic changes."""
        db = SessionLocal()
        try:
            sim = tradeoff_simulator_service.simulate_scenario(
                db=db,
                compute_capacity_change_pct=-20.0,
                traffic_growth_multiplier=1.2,
                commitments_coverage_pct=50.0,
                idle_cleanup_applied=True
            )
            self.assertGreater(sim["baseline_monthly_spend_usd"], 0)
            self.assertGreater(sim["projected_monthly_spend_usd"], 0)
            self.assertGreater(sim["savings_plan_discount_usd"], 0)
            self.assertIn(sim["operational_risk_level"], ["LOW", "ELEVATED", "CRITICAL"])
            self.assertTrue(len(sim["risk_summary"]) > 0)
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()
