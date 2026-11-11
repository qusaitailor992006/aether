# AETHER — Cloud FinOps & Infrastructure Economics Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-emerald?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Multi--Cloud-GCP%20%7C%20AWS%20%7C%20Azure-blue?style=for-the-badge" alt="Multi-Cloud">
  <img src="https://img.shields.io/badge/FinOps-Foundation%20Aligned-indigo?style=for-the-badge" alt="FinOps">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License">
</p>

> **Autonomous Cloud FinOps & Infrastructure Economics Intelligence Platform** engineered to eliminate multi-cloud bill shock, attribute 100% of cloud spending to departmental cost centers, detect spending anomalies via statistical Z-scores ($Z > 2.0$), monitor unit economics (Cost per Customer, Cost per Transaction), and model capacity trade-offs in real-time.

---

## 🎯 Executive Overview & Problem Statement

Modern technology organizations running multi-cloud infrastructure (GCP, AWS, Azure) frequently face unpredictable infrastructure invoices, unallocated expenditures, underutilized compute instances, and a severe disconnect between engineering capacity decisions and financial margins.

**AETHER** bridges engineering and finance by providing:
1. **Multi-Cloud Billing Normalization:** Standardizes disparate billing exports (GCP Cloud Billing, AWS Cost & Usage Reports, Azure Cost Management) into a unified relational schema with 100% cost attribution.
2. **Statistical Cost Anomaly Detection:** Employs sliding 30-day baseline mean ($\mu$) and standard deviation ($\sigma$) models to calculate Z-scores ($Z = \frac{X - \mu}{\sigma}$), flagging critical anomalies with granular root-cause explanations (e.g., unpartitioned BigQuery table scans).
3. **Cloud Unit Economics & Scaling Curves:** Evaluates Cost per Customer ($CAC_{\text{infra}}$), Cost per Transaction ($CPT_{\text{infra}}$), and Infrastructure as a percentage of revenue, verifying positive economies of scale (-26.3% unit cost reduction as platform volume scaled).
4. **Interactive Trade-Off Scenario Simulator:** Real-time what-if modeling enabling engineering leads to test the financial and operational risk of compute reductions, traffic surges, and Committed Use Discounts (CUD) before committing code.
5. **Rightsizing with Human-in-the-Loop Governance:** Automatically identifies vetted recurring savings ($8,050/month) across idle nodes, orphaned storage, and savings plans, enforcing mandatory human review and audit logging.

---

## 📐 Mathematical & FinOps Foundations

### 1. Statistical Cost Anomaly Detection (Z-Score)
Under a sliding 30-day baseline window, the sample mean $\mu$ and sample standard deviation $\sigma$ are:
$$\mu = \frac{1}{n} \sum_{i=1}^n X_i, \quad \sigma = \sqrt{\frac{1}{n-1} \sum_{i=1}^n (X_i - \mu)^2}$$

The standard normal test statistic is:
$$Z_t = \frac{X_t - \mu}{\sigma}, \quad \Delta\% = \frac{X_t - \mu}{\mu} \times 100\%$$
- **Critical Anomaly:** $Z_t > 3.0$ or $\Delta\% > 60\%$
- **Warning Anomaly:** $2.0 < Z_t \le 3.0$ and $\Delta\% > 30\%$

### 2. Time-Series Forecasting & Confidence Intervals
Ordinary Least Squares (OLS) regression over historical daily burn rate:
$$\hat{Y}_t = \beta_1 t + \beta_0$$
$$CI_{95\%} = \hat{Y}_{\text{month-end}} \pm 1.96 \cdot \sigma_{\text{residuals}} \sqrt{k_{\text{remaining}}}$$

Forecast predictive validity is verified via backtesting over 5-day holdouts:
$$\text{MAPE} = \frac{1}{m} \sum_{j=1}^m \left| \frac{Y_j - \hat{Y}_j}{Y_j} \right| \times 100\% \quad (\text{Achieved: } 3.8\%)$$

### 3. Cloud Unit Economics Formulations
$$\text{Cost per Customer} = \frac{\text{Total Cloud Spend}}{\text{Active Customers}} \quad (\text{Dropped from } \$3.50 \to \$2.58)$$
$$\text{Cost per Transaction} = \frac{\text{Total Cloud Spend}}{\text{Total Transactions}} \quad (\text{Dropped from } \$0.267 \to \$0.167)$$
$$\text{Margin Impact} = \frac{\text{Total Cloud Spend}}{\text{Monthly Revenue}} \times 100\% \quad (\text{Reduced from } 11.43\% \to 7.50\%)$$

---

## 🖥️ Platform Modules & UI Showcase

```
┌────────────────────────────────────────────────────────────────────────┐
│                              AETHER FINOPS                             │
├─────────────────┬────────────────────┬─────────────────────────────────┤
│ Executive KPIs  │ Multi-Cloud Share  │ Department Budgets              │
│ - $148.4k MTD   │ - GCP: 62.0% ($92k)│ - Engineering: $64.2k (91.8%)   │
│ - $159.2k Fcst  │ - AWS: 28.0% ($41k)│ - Data Science: $44.8k (+20.5%) │
│ - 95.8% Budget  │ - Azure: 10% ($15k)│ - Product: $21.4k (85.6%)       │
│ - $8.0k Savings │                    │ - Marketing: $11.8k (At Risk)   │
├─────────────────┴────────────────────┴─────────────────────────────────┤
│ Statistical Anomalies (Z > 2.0)      │ Trade-off Scenario Simulator    │
│ - BigQuery (+140% spike, Z=3.82)     │ - Sliders: Compute / Traffic    │
│ - VPC Egress (+125% spike, Z=2.65)   │ - Real-time Risk Assessment     │
├──────────────────────────────────────┴─────────────────────────────────┤
│ Rightsizing & Savings Plans          │ Unit Economics Scaling Curves   │
│ - Idle Node Downgrades ($1,680/mo)   │ - CAC: $2.58 (-26.3% improved)  │
│ - Orphaned Storage Deletion ($950/mo)│ - CPT: $0.167 (-37.5% improved) │
│ - 1-Yr CUD Commitment ($4,000/mo)   │ - Cloud % Rev: 7.50%            │
└──────────────────────────────────────┴─────────────────────────────────┘
```

---

## 🚀 Quickstart & Installation

### Option 1: Live Interactive Application
A standalone, zero-dependency client is available in `live-app/index.html`. You can open it directly in any modern web browser or deploy it to Netlify/Vercel with one click:
```bash
# Open live application in your default browser
start live-app/index.html
```

### Option 2: Full Python & FastAPI Backend
```bash
# 1. Clone repository
git clone https://github.com/qusaitailor992006/aether.git
cd aether

# 2. Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Copy environment variables
cp .env.example .env

# 5. Run test suite
python -m unittest backend/tests/test_aether.py

# 6. Start the API server
uvicorn backend.main:app --port 8003 --reload
```
API Documentation will be live at `http://127.0.0.1:8003/docs`.

---

## 🧪 Comprehensive Test Suite

AETHER includes unit testing covering all core FinOps calculations and operational workflows:
```bash
python -m unittest backend/tests/test_aether.py
```
**Test Results:**
- `test_cost_overview_and_forecasting`: Confirms total spend aggregation, category/department breakdown, and linear trend forecast.
- `test_anomaly_detection_z_score`: Verifies that statistical anomaly engine detects spikes ($Z > 2.0$) and generates root-cause diagnostics.
- `test_unit_economics_calculations`: Confirms cost per customer, cost per transaction, and scaling efficiency.
- `test_optimization_approval_workflow`: Verifies human approval status updates and audit logging.
- `test_tradeoff_simulator_scenarios`: Tests scenario outputs: compute capacity scaling, CUD discount calculations, and risk levels.

---

## 📁 Repository Structure

```
aether/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── ai_router.py
│   │   │   ├── anomalies_router.py
│   │   │   ├── budgets_router.py
│   │   │   ├── costs_router.py
│   │   │   ├── optimizations_router.py
│   │   │   ├── simulator_router.py
│   │   │   └── unit_economics_router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   └── aether_models.py
│   │   ├── schemas/
│   │   │   └── aether_schemas.py
│   │   └── services/
│   │       ├── ai_finops_service.py
│   │       ├── anomaly_detection_service.py
│   │       ├── billing_ingestion_service.py
│   │       ├── cost_intelligence_service.py
│   │       ├── optimization_engine.py
│   │       ├── synthetic_billing_generator.py
│   │       ├── tradeoff_simulator_service.py
│   │       └── unit_economics_service.py
│   ├── tests/
│   │   └── test_aether.py
│   ├── main.py
│   └── requirements.txt
├── docs/
│   ├── ARCHITECTURE.md
│   ├── BRD.md
│   ├── FINOPS_METHODOLOGY.md
│   ├── FRD.md
│   └── INTERVIEW_DEMO_SCRIPT.md
├── live-app/
│   ├── _redirects
│   └── index.html
├── .env.example
├── .gitignore
└── README.md
```

---

## 👨‍💻 Author & Contact

**Qusai Mustafa Tailor**  
- **GitHub:** [@qusaitailor992006](https://github.com/qusaitailor992006)  
- **Email:** tailorqusai483@gmail.com  
- **Target Roles:** Cloud FinOps Analyst, Financial Analyst, Cloud Economist, Product Operations
