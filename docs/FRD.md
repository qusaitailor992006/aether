# Functional Requirements Document (FRD)
## AETHER — Cloud FinOps & Infrastructure Economics Intelligence Platform

**Document Reference:** FRD-AETHER-2026-V1  
**Author:** Qusai Mustafa Tailor  
**System Version:** 1.0.0 Production  

---

## 1. System Scope & Core Capabilities
AETHER provides end-to-end cloud financial operations management:
1. **Multi-Cloud Billing Ingestion:** Ingest and normalize heterogeneous billing formats from GCP, AWS, and Azure into canonical records.
2. **Cost Intelligence & Allocation:** Aggregate expenditures across providers, services, departments, and environments with 100% attribution.
3. **Statistical Anomaly Detection:** Scan daily service spend using Z-scores and IQR to flag cost spikes.
4. **Cloud Unit Economics Engine:** Compute and track Cost per Customer, Cost per Transaction, and Infrastructure as % of Revenue.
5. **FinOps Rightsizing & Optimization:** Identify idle nodes, orphaned storage, and committed use discounts with human approval workflows.
6. **Scenario Trade-Off Simulator:** Interactive simulation engine projecting financial delta and operational risk under varying compute and traffic assumptions.
7. **AI FinOps Assistant:** Grounded natural-language query engine with deterministic offline analytical fallback.

---

## 2. Detailed Functional Specifications

### Module 1: Multi-Cloud Billing Ingestion
- **FR-1.1:** System shall ingest billing line items containing provider, service name, service category (Compute, Storage, Database, Networking, Egress), department, cost, usage, and timestamp.
- **FR-1.2:** System shall normalize provider-specific service names (e.g., `Google Compute Engine`, `Amazon EC2`, `Azure App Service`) into canonical category classifications.

### Module 2: Cost Intelligence & Time-Series Forecasting
- **FR-2.1:** System shall aggregate spend across 30-day trailing windows and calculate daily burn rate.
- **FR-2.2:** System shall forecast month-end spend using linear regression trend extrapolation:
  $$\hat{Y}_{t} = \hat{\beta}_1 t + \hat{\beta}_0$$
- **FR-2.3:** System shall calculate 95% forecast confidence intervals:
  $$CI_{95\%} = \hat{Y}_{\text{total}} \pm 1.96 \cdot \sigma_{\text{residuals}} \sqrt{N_{\text{remaining}}}$$
- **FR-2.4:** System shall evaluate forecast accuracy using Mean Absolute Percentage Error (MAPE) backtesting over trailing 5-day windows.

### Module 3: Statistical Anomaly Detection
- **FR-3.1:** System shall compute daily service-level mean ($\mu$) and standard deviation ($\sigma$).
- **FR-3.2:** System shall compute Z-score for incoming daily spend $X$:
  $$Z = \frac{X - \mu}{\sigma}$$
- **FR-3.3:** Flag cost spike as anomaly if $Z > 2.0$ and percentage increase $> 30\%$.
- **FR-3.4:** Assign severity:
  - `CRITICAL` if $Z > 3.0$ or spike $> 60\%$
  - `WARNING` if $Z > 2.0$ or spike $> 30\%$
  - `INFO` otherwise.

### Module 4: Cloud Unit Economics
- **FR-4.1 Cost per Active Customer:**
  $$\text{Unit Cost}_{\text{customer}} = \frac{\text{Total Cloud Spend}}{\text{Active Customers}}$$
- **FR-4.2 Cost per Transaction:**
  $$\text{Unit Cost}_{\text{transaction}} = \frac{\text{Total Cloud Spend}}{\text{Monthly Transactions}}$$
- **FR-4.3 Infrastructure Cost % of Revenue:**
  $$\text{Infrastructure Margin Impact} = \frac{\text{Total Cloud Spend}}{\text{Total Monthly Revenue}} \times 100\%$$

### Module 5: Rightsizing & Optimization Engine
- **FR-5.1:** Identify underutilized compute instances (CPU $< 18\%$, Memory $< 25\%$ over 30 days).
- **FR-5.2:** Detect unattached persistent disks and orphaned EBS storage detached for $> 30$ days.
- **FR-5.3:** Identify steady-state baseline compute suitable for 1-year / 3-year Committed Use Discounts (yielding $\approx 32\%$ discount).
- **FR-5.4:** Enforce human review approval state (`PENDING_APPROVAL`, `APPROVED`, `DISMISSED`) and log all approval events into `FinOpsAuditLog`.
