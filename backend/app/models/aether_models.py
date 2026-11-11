import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Text
from backend.app.core.database import Base

class CloudBillingRecord(Base):
    __tablename__ = "cloud_billing_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    record_id = Column(String, unique=True, index=True)
    provider = Column(String, index=True) # GCP, AWS, Azure
    service_name = Column(String, index=True) # e.g., Cloud Run, BigQuery, AWS EC2, S3
    service_category = Column(String, index=True) # Compute, Storage, Database, Networking, Egress
    resource_id = Column(String, index=True)
    department = Column(String, index=True) # Engineering, Data Science, Marketing, Product, Operations
    project_id = Column(String, index=True)
    environment = Column(String, index=True) # Production, Staging, Development
    cost_usd = Column(Float, nullable=False)
    usage_amount = Column(Float, default=1.0)
    usage_unit = Column(String, default="hours")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class DepartmentBudget(Base):
    __tablename__ = "department_budgets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    department = Column(String, unique=True, index=True)
    monthly_budget_usd = Column(Float, nullable=False)
    current_spend_usd = Column(Float, default=0.0)
    forecasted_spend_usd = Column(Float, default=0.0)
    variance_pct = Column(Float, default=0.0)
    status = Column(String, default="WITHIN_BUDGET") # WITHIN_BUDGET, AT_RISK, EXCEEDED
    month = Column(String, default="2026-11")

class CloudAnomaly(Base):
    __tablename__ = "cloud_anomalies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    anomaly_id = Column(String, unique=True, index=True)
    service_name = Column(String, index=True)
    department = Column(String, index=True)
    date = Column(String, index=True)
    expected_cost_usd = Column(Float, nullable=False)
    actual_cost_usd = Column(Float, nullable=False)
    spike_pct = Column(Float, nullable=False)
    z_score = Column(Float, nullable=False)
    severity = Column(String, default="WARNING") # CRITICAL, WARNING, INFO
    root_cause_explanation = Column(Text)
    status = Column(String, default="OPEN") # OPEN, INVESTIGATING, RESOLVED

class OptimizationRecommendation(Base):
    __tablename__ = "optimization_recommendations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    recommendation_id = Column(String, unique=True, index=True)
    resource_id = Column(String, index=True)
    service_name = Column(String, index=True)
    department = Column(String, index=True)
    optimization_type = Column(String) # IDLE_RESOURCE, RIGHTSIZING, UNATTACHED_STORAGE, SAVINGS_PLAN
    current_monthly_cost_usd = Column(Float, nullable=False)
    estimated_monthly_savings_usd = Column(Float, nullable=False)
    effort = Column(String, default="LOW") # LOW, MEDIUM, HIGH
    confidence_score = Column(Float, default=0.95)
    justification = Column(Text)
    human_approval_status = Column(String, default="PENDING_APPROVAL") # PENDING_APPROVAL, APPROVED, DISMISSED

class UnitEconomicsMetric(Base):
    __tablename__ = "unit_economics_metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(String, unique=True, index=True)
    active_customers = Column(Integer, nullable=False)
    monthly_transactions = Column(Integer, nullable=False)
    api_requests_millions = Column(Float, nullable=False)
    monthly_revenue_usd = Column(Float, nullable=False)
    total_cloud_spend_usd = Column(Float, nullable=False)
    cost_per_customer_usd = Column(Float, nullable=False)
    cost_per_transaction_usd = Column(Float, nullable=False)
    cost_per_million_api_requests_usd = Column(Float, nullable=False)
    cloud_spend_pct_of_revenue = Column(Float, nullable=False)

class FinOpsAuditLog(Base):
    __tablename__ = "finops_audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    user_email = Column(String, default="finops-lead@enterprise.com")
    details = Column(Text)
