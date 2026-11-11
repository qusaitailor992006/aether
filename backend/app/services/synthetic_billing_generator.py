import uuid
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.app.models.aether_models import (
    CloudBillingRecord,
    DepartmentBudget,
    CloudAnomaly,
    OptimizationRecommendation,
    UnitEconomicsMetric,
    FinOpsAuditLog
)

class SyntheticBillingGenerator:
    def seed_initial_enterprise_data(self, db: Session):
        """
        Populates database with realistic enterprise multi-cloud billing records,
        department budgets, cost anomalies, unit economics, and rightsizing opportunities.
        """
        # Idempotency check
        if db.query(DepartmentBudget).count() > 0:
            return

        # 1. Seed Department Budgets
        budgets = [
            DepartmentBudget(
                id=str(uuid.uuid4()),
                department="Engineering",
                monthly_budget_usd=70000.0,
                current_spend_usd=64250.0,
                forecasted_spend_usd=68500.0,
                variance_pct=-2.1,
                status="WITHIN_BUDGET",
                month="2026-11"
            ),
            DepartmentBudget(
                id=str(uuid.uuid4()),
                department="Data Science",
                monthly_budget_usd=40000.0,
                current_spend_usd=44800.0,
                forecasted_spend_usd=48200.0,
                variance_pct=20.5,
                status="EXCEEDED",
                month="2026-11"
            ),
            DepartmentBudget(
                id=str(uuid.uuid4()),
                department="Product",
                monthly_budget_usd=25000.0,
                current_spend_usd=21400.0,
                forecasted_spend_usd=23100.0,
                variance_pct=-7.6,
                status="WITHIN_BUDGET",
                month="2026-11"
            ),
            DepartmentBudget(
                id=str(uuid.uuid4()),
                department="Marketing",
                monthly_budget_usd=12000.0,
                current_spend_usd=11800.0,
                forecasted_spend_usd=12500.0,
                variance_pct=4.1,
                status="AT_RISK",
                month="2026-11"
            ),
            DepartmentBudget(
                id=str(uuid.uuid4()),
                department="Operations",
                monthly_budget_usd=8000.0,
                current_spend_usd=6200.0,
                forecasted_spend_usd=6900.0,
                variance_pct=-13.7,
                status="WITHIN_BUDGET",
                month="2026-11"
            )
        ]
        db.bulk_save_objects(budgets)

        # 2. Seed Billing Records (Last 30 Days)
        providers_services = [
            ("GCP", "Compute Engine", "Compute", "Engineering", 1100.0),
            ("GCP", "BigQuery", "Database", "Data Science", 950.0),
            ("GCP", "Cloud Run", "Compute", "Product", 420.0),
            ("GCP", "Cloud Storage", "Storage", "Engineering", 380.0),
            ("GCP", "Cloud SQL", "Database", "Engineering", 620.0),
            ("AWS", "Amazon EC2", "Compute", "Engineering", 850.0),
            ("AWS", "Amazon S3", "Storage", "Data Science", 310.0),
            ("AWS", "Amazon RDS", "Database", "Product", 490.0),
            ("Azure", "Azure App Service", "Compute", "Marketing", 280.0),
            ("GCP", "Cloud NAT & VPC", "Networking", "Engineering", 220.0)
        ]

        now = datetime.utcnow()
        records = []
        random.seed(42)

        for day_offset in range(30, -1, -1):
            date_val = now - timedelta(days=day_offset)
            for provider, service, cat, dept, base_cost in providers_services:
                # Add natural noise and slight weekday seasonality
                noise = random.uniform(-0.08, 0.08)
                daily_cost = base_cost * (1.0 + noise)
                
                # Introduce a controlled BigQuery spike 4 days ago
                if service == "BigQuery" and day_offset == 4:
                    daily_cost *= 2.4 # Controlled anomaly

                rec = CloudBillingRecord(
                    id=str(uuid.uuid4()),
                    record_id=f"REC-{uuid.uuid4().hex[:8].upper()}",
                    provider=provider,
                    service_name=service,
                    service_category=cat,
                    resource_id=f"{service.lower().replace(' ', '-')}-{dept.lower()[:3]}",
                    department=dept,
                    project_id=f"proj-{dept.lower()}-core",
                    environment="Production" if day_offset % 3 != 0 else "Staging",
                    cost_usd=round(daily_cost, 2),
                    usage_amount=24.0,
                    usage_unit="hours",
                    timestamp=date_val
                )
                records.append(rec)

        db.bulk_save_objects(records)

        # 3. Seed Realistic Cloud Anomalies
        anomalies = [
            CloudAnomaly(
                id=str(uuid.uuid4()),
                anomaly_id="ANOM-2026-001",
                service_name="BigQuery",
                department="Data Science",
                date=(now - timedelta(days=4)).strftime("%Y-%m-%d"),
                expected_cost_usd=950.0,
                actual_cost_usd=2280.0,
                spike_pct=140.0,
                z_score=3.82,
                severity="CRITICAL",
                root_cause_explanation="Unpartitioned table scan in user recommendation training pipeline triggered 8.4 TB slot consumption in on-demand pricing tier.",
                status="OPEN"
            ),
            CloudAnomaly(
                id=str(uuid.uuid4()),
                anomaly_id="ANOM-2026-002",
                service_name="Cloud NAT & VPC",
                department="Engineering",
                date=(now - timedelta(days=9)).strftime("%Y-%m-%d"),
                expected_cost_usd=220.0,
                actual_cost_usd=495.0,
                spike_pct=125.0,
                z_score=2.65,
                severity="WARNING",
                root_cause_explanation="Cross-region egress surge between us-central1 and europe-west1 caused by uncompressed model artifact synchronisation.",
                status="RESOLVED"
            ),
            CloudAnomaly(
                id=str(uuid.uuid4()),
                anomaly_id="ANOM-2026-003",
                service_name="Amazon RDS",
                department="Product",
                date=(now - timedelta(days=16)).strftime("%Y-%m-%d"),
                expected_cost_usd=490.0,
                actual_cost_usd=810.0,
                spike_pct=65.3,
                z_score=2.18,
                severity="WARNING",
                root_cause_explanation="Provisioned IOPS autoscale trigger exceeded baseline threshold during automated batch customer migration.",
                status="INVESTIGATING"
            )
        ]
        db.bulk_save_objects(anomalies)

        # 4. Seed FinOps Rightsizing & Optimization Recommendations
        optimizations = [
            OptimizationRecommendation(
                id=str(uuid.uuid4()),
                recommendation_id="OPT-2026-01",
                resource_id="gce-worker-pool-eng",
                service_name="Compute Engine",
                department="Engineering",
                optimization_type="RIGHTSIZING",
                current_monthly_cost_usd=4800.0,
                estimated_monthly_savings_usd=1680.0,
                effort="LOW",
                confidence_score=0.96,
                justification="12 compute nodes running n2-standard-16 have maintained < 18% CPU and < 24% memory utilization over the past 30 days. Downgrade to n2-standard-8.",
                human_approval_status="PENDING_APPROVAL"
            ),
            OptimizationRecommendation(
                id=str(uuid.uuid4()),
                recommendation_id="OPT-2026-02",
                resource_id="ebs-vol-orphan-staging",
                service_name="Amazon S3 / EBS",
                department="Data Science",
                optimization_type="UNATTACHED_STORAGE",
                current_monthly_cost_usd=950.0,
                estimated_monthly_savings_usd=950.0,
                effort="LOW",
                confidence_score=0.99,
                justification="48 unattached gp3 EBS volumes (total 9.6 TB) detached for > 45 days following ML training cluster shutdown.",
                human_approval_status="APPROVED"
            ),
            OptimizationRecommendation(
                id=str(uuid.uuid4()),
                recommendation_id="OPT-2026-03",
                resource_id="cloudsql-prod-db-replica",
                service_name="Cloud SQL",
                department="Engineering",
                optimization_type="IDLE_RESOURCE",
                current_monthly_cost_usd=1420.0,
                estimated_monthly_savings_usd=1420.0,
                effort="MEDIUM",
                confidence_score=0.91,
                justification="Staging database replica in us-east1 has received 0 read queries for 28 consecutive days.",
                human_approval_status="PENDING_APPROVAL"
            ),
            OptimizationRecommendation(
                id=str(uuid.uuid4()),
                recommendation_id="OPT-2026-04",
                resource_id="gcp-compute-cud-plan",
                service_name="Compute Engine",
                department="Engineering",
                optimization_type="SAVINGS_PLAN",
                current_monthly_cost_usd=12500.0,
                estimated_monthly_savings_usd=4000.0,
                effort="LOW",
                confidence_score=0.98,
                justification="Baseline compute footprint exceeds 120 vCPUs consistently. Enrolling in 1-Year Committed Use Discount yields guaranteed 32% discount.",
                human_approval_status="PENDING_APPROVAL"
            )
        ]
        db.bulk_save_objects(optimizations)

        # 5. Seed Historical Unit Economics (Last 6 Months)
        unit_metrics = [
            UnitEconomicsMetric(
                id=str(uuid.uuid4()),
                date="2026-06",
                active_customers=32000,
                monthly_transactions=420000,
                api_requests_millions=14.5,
                monthly_revenue_usd=980000.0,
                total_cloud_spend_usd=112000.0,
                cost_per_customer_usd=3.50,
                cost_per_transaction_usd=0.267,
                cost_per_million_api_requests_usd=7724.1,
                cloud_spend_pct_of_revenue=11.43
            ),
            UnitEconomicsMetric(
                id=str(uuid.uuid4()),
                date="2026-07",
                active_customers=36500,
                monthly_transactions=490000,
                api_requests_millions=17.2,
                monthly_revenue_usd=1140000.0,
                total_cloud_spend_usd=119500.0,
                cost_per_customer_usd=3.27,
                cost_per_transaction_usd=0.244,
                cost_per_million_api_requests_usd=6947.6,
                cloud_spend_pct_of_revenue=10.48
            ),
            UnitEconomicsMetric(
                id=str(uuid.uuid4()),
                date="2026-08",
                active_customers=41200,
                monthly_transactions=580000,
                api_requests_millions=21.0,
                monthly_revenue_usd=1320000.0,
                total_cloud_spend_usd=128000.0,
                cost_per_customer_usd=3.10,
                cost_per_transaction_usd=0.221,
                cost_per_million_api_requests_usd=6095.2,
                cloud_spend_pct_of_revenue=9.70
            ),
            UnitEconomicsMetric(
                id=str(uuid.uuid4()),
                date="2026-09",
                active_customers=46000,
                monthly_transactions=675000,
                api_requests_millions=25.4,
                monthly_revenue_usd=1520000.0,
                total_cloud_spend_usd=136200.0,
                cost_per_customer_usd=2.96,
                cost_per_transaction_usd=0.202,
                cost_per_million_api_requests_usd=5362.2,
                cloud_spend_pct_of_revenue=8.96
            ),
            UnitEconomicsMetric(
                id=str(uuid.uuid4()),
                date="2026-10",
                active_customers=51800,
                monthly_transactions=780000,
                api_requests_millions=29.8,
                monthly_revenue_usd=1740000.0,
                total_cloud_spend_usd=144500.0,
                cost_per_customer_usd=2.79,
                cost_per_transaction_usd=0.185,
                cost_per_million_api_requests_usd=4848.9,
                cloud_spend_pct_of_revenue=8.30
            ),
            UnitEconomicsMetric(
                id=str(uuid.uuid4()),
                date="2026-11",
                active_customers=57400,
                monthly_transactions=890000,
                api_requests_millions=34.5,
                monthly_revenue_usd=1980000.0,
                total_cloud_spend_usd=148450.0,
                cost_per_customer_usd=2.58,
                cost_per_transaction_usd=0.167,
                cost_per_million_api_requests_usd=4302.9,
                cloud_spend_pct_of_revenue=7.50
            )
        ]
        db.bulk_save_objects(unit_metrics)
        db.commit()

synthetic_billing_generator = SyntheticBillingGenerator()
