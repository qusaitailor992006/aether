from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class BillingRecordCreate(BaseModel):
    provider: str
    service_name: str
    service_category: str
    resource_id: str
    department: str
    project_id: str
    environment: str
    cost_usd: float
    usage_amount: float = 1.0
    usage_unit: str = "hours"

class CostOverviewResponse(BaseModel):
    total_monthly_spend_usd: float
    forecasted_monthly_spend_usd: float
    total_budget_usd: float
    budget_utilization_pct: float
    spend_by_category: Dict[str, float]
    spend_by_department: Dict[str, float]
    spend_by_provider: Dict[str, float]
    daily_spend_trend: List[Dict[str, Any]]

class DepartmentBudgetSchema(BaseModel):
    department: str
    monthly_budget_usd: float
    current_spend_usd: float
    forecasted_spend_usd: float
    variance_pct: float
    status: str

class AnomalySchema(BaseModel):
    anomaly_id: str
    service_name: str
    department: str
    date: str
    expected_cost_usd: float
    actual_cost_usd: float
    spike_pct: float
    z_score: float
    severity: str
    root_cause_explanation: str
    status: str

class OptimizationRecommendationSchema(BaseModel):
    recommendation_id: str
    resource_id: str
    service_name: str
    department: str
    optimization_type: str
    current_monthly_cost_usd: float
    estimated_monthly_savings_usd: float
    effort: str
    confidence_score: float
    justification: str
    human_approval_status: str

class UnitEconomicsSchema(BaseModel):
    date: str
    active_customers: int
    monthly_transactions: int
    api_requests_millions: float
    monthly_revenue_usd: float
    total_cloud_spend_usd: float
    cost_per_customer_usd: float
    cost_per_transaction_usd: float
    cost_per_million_api_requests_usd: float
    cloud_spend_pct_of_revenue: float

class ScenarioSimRequest(BaseModel):
    compute_capacity_change_pct: float = Field(0.0, description="Percentage change in compute (-50 to +100)")
    traffic_growth_multiplier: float = Field(1.0, description="Traffic multiplier e.g. 1.5 for 50% growth")
    commitments_coverage_pct: float = Field(0.0, description="Coverage by 1-year or 3-year Savings Plans (0 to 100)")
    idle_cleanup_applied: bool = Field(True, description="Whether to decommission flagged idle resources")

class ScenarioSimResponse(BaseModel):
    baseline_monthly_spend_usd: float
    projected_monthly_spend_usd: float
    monthly_delta_usd: float
    delta_pct: float
    compute_delta_usd: float
    storage_delta_usd: float
    savings_plan_discount_usd: float
    operational_risk_level: str
    risk_summary: str

class AIQueryRequest(BaseModel):
    query: str

class AIQueryResponse(BaseModel):
    query: str
    answer: str
    evidence: Dict[str, Any]
    source: str
