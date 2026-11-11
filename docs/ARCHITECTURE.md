# Architecture & System Design
## AETHER — Cloud FinOps & Infrastructure Economics Intelligence Platform

**Lead Architect:** Qusai Mustafa Tailor  
**System Class:** Enterprise Multi-Cloud Financial Operations Platform  

---

## 1. High-Level System Architecture

```
                    ┌────────────────────────────────────────────────────────┐
                    │               Client Layer (Dual Access)               │
                    │  - Standalone Netlify SPA (Interactive Dark-Mode UI)   │
                    │  - In-browser scenario simulator & AI query interface  │
                    └───────────────────────────┬────────────────────────────┘
                                                │ REST API / JSON
                                                ▼
                    ┌────────────────────────────────────────────────────────┐
                    │              FastAPI Backend Gateway (Port 8003)       │
                    │  - Multi-Cloud Billing Ingest & Normalization          │
                    │  - Pydantic v2 Schema Validation & CORS Middleware     │
                    └───────┬───────────────────┬───────────────────┬────────┘
                            │                   │                   │
                            ▼                   ▼                   ▼
    ┌─────────────────────────────┐ ┌─────────────────────┐ ┌───────────────────────┐
    │ Cost Intelligence & Forecast│ │ Anomaly & Z-Score Svc││ Optimization Engine   │
    │  - Multi-Cloud Aggregation  │ │ - 30-day baseline   │ │ - Idle VM detection   │
    │  - OLS Trend Extrapolation  │ │ - Outlier detection │ │ - Orphaned storage    │
    │  - 95% Confidence Bounds    │ │ - Root-cause analysis││ - 1-Yr/3-Yr CUD plans │
    └──────────────┬──────────────┘ └──────────┬──────────┘ └───────────┬───────────┘
                   │                           │                        │
                   └───────────────────────────┼────────────────────────┘
                                               │ SQLAlchemy ORM (WAL Mode)
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │                   Data Persistence Layer               │
                    │  - SQLite (Production-grade with WAL Pragmas)          │
                    │  - Multi-Cloud Schema: billing_records, budgets,       │
                    │    anomalies, optimizations, unit_economics, audit_logs│
                    └────────────────────────────────────────────────────────┘
```

---

## 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    DEPARTMENT_BUDGET ||--o{ CLOUD_BILLING_RECORD : allocates
    CLOUD_BILLING_RECORD ||--o{ CLOUD_ANOMALY : manifests_in
    CLOUD_BILLING_RECORD ||--o{ OPTIMIZATION_RECOMMENDATION : evaluated_in
    OPTIMIZATION_RECOMMENDATION ||--o{ FINOPS_AUDIT_LOG : tracks_approval

    CLOUD_BILLING_RECORD {
        string id PK
        string record_id UK
        string provider
        string service_name
        string service_category
        string resource_id
        string department
        string project_id
        string environment
        float cost_usd
        float usage_amount
        string usage_unit
        datetime timestamp
    }

    DEPARTMENT_BUDGET {
        string id PK
        string department UK
        float monthly_budget_usd
        float current_spend_usd
        float forecasted_spend_usd
        float variance_pct
        string status
        string month
    }

    CLOUD_ANOMALY {
        string id PK
        string anomaly_id UK
        string service_name
        string department
        string date
        float expected_cost_usd
        float actual_cost_usd
        float spike_pct
        float z_score
        string severity
        string root_cause_explanation
        string status
    }

    OPTIMIZATION_RECOMMENDATION {
        string id PK
        string recommendation_id UK
        string resource_id
        string service_name
        string department
        string optimization_type
        float current_monthly_cost_usd
        float estimated_monthly_savings_usd
        string effort
        float confidence_score
        string justification
        string human_approval_status
    }

    UNIT_ECONOMICS_METRIC {
        string id PK
        string date UK
        int active_customers
        int monthly_transactions
        float api_requests_millions
        float monthly_revenue_usd
        float total_cloud_spend_usd
        float cost_per_customer_usd
        float cost_per_transaction_usd
        float cost_per_million_api_requests_usd
        float cloud_spend_pct_of_revenue
    }

    FINOPS_AUDIT_LOG {
        string id PK
        datetime timestamp
        string action
        string entity_type
        string entity_id
        string user_email
        string details
    }
```

---

## 3. Reliability & Security Controls
1. **Zero Secret Leakage:** Groq API keys and credentials reside strictly in `.env` (guarded by `.gitignore`).
2. **Deterministic FinOps Fallback:** If LLM inference is disabled, the AI FinOps Assistant operates on deterministic SQL/Python analytical rules with zero hallucinations.
3. **Audit Trail Governance:** No rightsizing action or resource decommissioning is applied automatically; every approval requires human intervention and is permanently logged with timestamps and user emails.
