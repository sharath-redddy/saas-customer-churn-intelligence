# SaaS Customer Churn Intelligence Platform

## Enterprise Churn Analytics | BigQuery, XGBoost & Power BI

---

## Project Overview

This project is an end-to-end **SaaS Customer Churn Intelligence Platform** built to simulate a real enterprise analytics workflow for a B2B SaaS company.

The solution helps leadership and customer success teams identify customers at risk of churn, quantify Monthly Recurring Revenue exposure, monitor risk movement over time, prioritize retention outreach, and understand account-level churn drivers.

The project uses **Python** for synthetic enterprise data generation and machine learning, **Google BigQuery** for cloud data warehousing and SQL analytics, **XGBoost** for churn prediction, and **Power BI** for executive dashboards.

---

## Business Problem

SaaS businesses rely heavily on recurring revenue. Customer churn directly impacts Monthly Recurring Revenue, customer lifetime value, growth forecasting, and profitability.

The business needs to answer:

* Which customers are most likely to churn?
* How much MRR is currently at risk?
* Which accounts became riskier this month?
* Which industries or segments are driving churn risk?
* Which customers should the retention team contact first?
* What action should customer success take for each account?

This project solves those questions through a complete analytics and business intelligence workflow.

---

## Project Objectives

The main objectives of this project are:

1. Generate a realistic B2B SaaS customer-month dataset.
2. Build a cloud data warehouse layer using BigQuery.
3. Create SQL-based churn metrics, risk scoring, and migration logic.
4. Train a churn prediction model using XGBoost.
5. Build an advanced Power BI dashboard for executives and customer success teams.
6. Translate analytics into business recommendations and retention actions.

---

## Tech Stack

| Layer                | Tools Used            |
| -------------------- | --------------------- |
| Data Generation      | Python, Pandas, NumPy |
| Cloud Data Warehouse | Google BigQuery       |
| SQL Analytics        | BigQuery Standard SQL |
| Machine Learning     | XGBoost, Scikit-learn |
| Data Visualization   | Power BI              |
| Version Control      | GitHub                |

---

## Repository Structure

```text
saas-customer-churn-intelligence/
│
├── data/
│   └── saas_customer_churn.csv
│
├── scripts/
│   ├── generate_saas_churn_data.py
│   └── train_churn_xgboost.py
│
├── sql/
│   ├── 01_create_bigquery_tables.sql
│   ├── 02_create_analytics_table.sql
│   ├── 03_churn_metrics_and_risk_scores.sql
│   └── 04_customer_risk_migration.sql
│
├── dashboard/
│   ├── saas_churn_powerbi_dashboard.pbix
│   └── saas_churn_powerbi_dashboard.pdf
│
├── images/
│   ├── executive_risk_movement.png
│   ├── retention_operations_cockpit.png
│   └── customer_360_risk_profile.png
│
├── outputs/
│   ├── model_metrics.csv
│   ├── feature_importance.csv
│   └── feature_importance_top15.png
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Dataset

The dataset was synthetically generated to represent a realistic B2B SaaS business.

Each row represents one company’s monthly subscription, product usage, support activity, revenue, and churn status.

### Dataset Summary

| Metric             |                Value |
| ------------------ | -------------------: |
| Total Records      |               22,082 |
| Unique Companies   |                3,000 |
| Date Range         | Jan 2024 to Jun 2025 |
| Overall Churn Rate |               11.98% |

### Key Features

| Feature              | Description                               |
| -------------------- | ----------------------------------------- |
| company_id           | Unique customer account ID                |
| billing_month        | Monthly billing period                    |
| industry             | Customer industry                         |
| region               | Customer region                           |
| company_size         | Small Business, Mid Market, or Enterprise |
| subscription_tier    | Bronze, Silver, or Gold                   |
| contract_type        | Monthly or Annual                         |
| seats_purchased      | Number of purchased seats                 |
| active_users         | Monthly active users                      |
| support_tickets      | Number of support tickets raised          |
| feature_usage_score  | Product adoption score from 0 to 100      |
| account_health_score | Health indicator from 0 to 100            |
| tenure_months        | Customer tenure                           |
| mrr                  | Monthly Recurring Revenue                 |
| churn                | Churn target variable                     |
| customer_status      | Active or Churned                         |

---

## Data Architecture

The project follows a modern analytics architecture:

```text
Python Synthetic Data Generation
        ↓
BigQuery Raw Layer
        ↓
BigQuery Analytics Layer
        ↓
SQL Metrics, Risk Scoring & Risk Migration
        ↓
XGBoost Churn Prediction Model
        ↓
Power BI Executive Dashboard
```

---

## BigQuery Data Warehouse Design

### 1. Raw Layer

The raw table stores the original generated SaaS churn dataset.

```text
saas_churn_raw.saas_customer_churn_raw
```

### 2. Analytics Layer

The analytics table enriches the raw data with business-ready features such as billing year, billing month label, adoption rate, health segment, and churn risk reason.

```text
saas_churn_analytics.customer_churn_monthly
```

### 3. Risk Scoring Layer

The risk scoring table assigns a churn risk score and risk band to every customer-month record.

```text
saas_churn_analytics.customer_churn_risk_scores
```

### 4. Risk Migration Layer

The risk migration table tracks how each customer moved between risk bands month-over-month.

```text
saas_churn_analytics.customer_risk_migration
```

---

## SQL Analytics

The project includes BigQuery SQL scripts for:

* Dataset and table creation
* Curated analytics table creation
* Monthly churn rate
* MRR churn rate
* User engagement cohorts
* Churn risk score calculation
* Customer risk band assignment
* Month-over-month risk migration analysis

### Risk Band Validation

| Risk Band     | Customer Months | Churn Rate | Total MRR |
| ------------- | --------------: | ---------: | --------: |
| Critical Risk |           2,472 |     21.32% |    $5.79M |
| High Risk     |           5,508 |     18.03% |   $27.88M |
| Medium Risk   |           9,198 |      9.56% |   $46.52M |
| Low Risk      |           4,904 |      5.02% |   $23.05M |

The validation confirms that higher-risk segments have significantly higher churn rates, making the risk scoring logic useful for business decision-making.

---

## Risk Migration Analysis

A major feature of this project is the **Customer Risk Migration** layer.

Instead of only showing which customers are currently high risk, the dashboard identifies:

* Which customers became riskier this month
* Which customers improved
* Which customers stayed stable
* How much MRR moved into higher-risk categories
* Which industries are driving risk deterioration
* Which accounts need executive attention

This transforms the dashboard from a static reporting tool into a decision-support system for customer retention.

---

## Machine Learning Model

An XGBoost classifier was trained to predict customer churn using subscription, revenue, usage, support, and account health features.

### Model Performance

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 66.04% |
| Precision | 19.64% |
| Recall    | 59.36% |
| F1 Score  | 29.51% |
| ROC-AUC   | 67.08% |

For churn use cases, recall is especially important because the business wants to identify as many potential churners as possible before they leave.

The model is designed to support a retention workflow where customer success teams review predicted high-risk accounts and prioritize outreach.

### Top Churn Drivers

The XGBoost model identified the following major churn drivers:

1. Customer health segment
2. Monthly contract type
3. Low usage and high support burden
4. User adoption rate
5. Subscription tier
6. Account health score
7. Feature usage score
8. Billing month pattern
9. Monthly recurring revenue
10. Customer tenure

---

## Power BI Dashboard

The final Power BI dashboard contains three advanced pages.

---

## Page 1: Executive Risk Movement Command Center

<img width="1920" height="1200" alt="Executive Risk Command Center" src="https://github.com/user-attachments/assets/b88e1b28-d899-460d-833e-844b399c7601" />


This page is designed for executive leadership.

It shows month-over-month customer risk movement and highlights where revenue exposure is increasing.

### Key Features

* Current MRR
* MRR at risk
* Worsened MRR
* Worsened accounts
* Improved accounts
* Average risk score
* Customer risk migration matrix
* Account movement status
* MRR exposure by migration path
* Industries driving risk deterioration
* Executive watchlist of deteriorating accounts
* Executive insight summary

### Business Value

This page helps leadership understand not just current churn risk, but how customer risk is changing over time.

---

## Page 2: Retention Operations Cockpit

<img width="1920" height="1200" alt="Retention Operations Cockpit" src="https://github.com/user-attachments/assets/534e23b8-2b78-44e5-8034-677d6da9a3a4" />


This page is designed for customer success and retention teams.

It converts analytics into a prioritized action queue.

### Key Features

* Retention queue accounts
* Retention queue MRR
* P1 immediate action accounts
* P1 MRR exposure
* Average retention priority score
* Retention action queue
* Account risk map
* Primary churn risk drivers
* MRR exposure by recommended action
* Retention priority distribution

### Business Value

This page helps customer success teams identify which customers to contact first, why they are at risk, and what retention action should be taken.

---

## Page 3: Customer 360 Risk Profile

<img width="1770" height="1020" alt="Customer 360 Risk Profile" src="https://github.com/user-attachments/assets/c67120bb-51e5-422a-99df-3bc98e6b3488" />


This page provides account-level analysis for customer success teams.

Users can select an account and view the full customer risk profile.

### Key Features

* Account selector
* Current MRR
* Risk band
* Risk score
* Risk movement
* Health score
* Risk score trend
* MRR trend
* Feature usage trend
* Support ticket trend
* Monthly account history
* Recommended next-best action

### Business Value

This page allows customer success teams to investigate individual accounts and understand the reason behind each customer’s churn risk.

---

## Business Recommendations

Based on the analysis, the following actions are recommended:

1. Prioritize accounts that worsened into Critical or High Risk segments.
2. Focus retention outreach on high-MRR customers with low usage and high support tickets.
3. Offer annual contract incentives to monthly customers with high churn risk.
4. Launch product adoption campaigns for accounts with weak feature usage.
5. Assign specialist support to customers with high ticket volume.
6. Monitor risk migration monthly to detect early deterioration.
7. Use Customer 360 analysis before retention calls to personalize outreach.

---

## Business Impact

This solution enables a SaaS business to:

* Detect churn risk earlier
* Quantify revenue exposure
* Prioritize customer success resources
* Improve retention planning
* Reduce preventable MRR churn
* Support data-driven executive decision-making

---

## How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/sharath-redddy/saas-customer-churn-intelligence.git
cd saas-customer-churn-intelligence
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Synthetic Data

```bash
python scripts/generate_saas_churn_data.py
```

This creates:

```text
data/saas_customer_churn.csv
```

### 4. Load Data into BigQuery

Upload the generated CSV into:

```text
sage-momentum-472609-n9.saas_churn_raw.saas_customer_churn_raw
```

### 5. Run SQL Scripts

Run the SQL scripts in this order:

```text
sql/01_create_bigquery_tables.sql
sql/02_create_analytics_table.sql
sql/03_churn_metrics_and_risk_scores.sql
sql/04_customer_risk_migration.sql
```

### 6. Train the Machine Learning Model

```bash
python scripts/train_churn_xgboost.py
```

The model exports metrics and feature importance files into the `outputs/` folder.

### 7. Open Power BI Dashboard

Open:

```text
dashboard/saas_churn_powerbi_dashboard.pbix
```

---

## Key Skills Demonstrated

* End-to-end analytics project development
* Synthetic enterprise data generation
* Cloud data warehousing with BigQuery
* SQL transformation and analytics modeling
* SaaS KPI development
* Churn risk scoring
* Customer risk migration analysis
* Machine learning with XGBoost
* Feature importance interpretation
* Power BI dashboard design
* Customer success action queue design
* Executive storytelling
* Business recommendations from data

---

## Project Highlights

* Generated 22K+ customer-month records for a realistic B2B SaaS business.
* Built BigQuery analytics tables for churn, MRR, engagement, and risk scoring.
* Created customer risk migration logic to track month-over-month risk movement.
* Trained an XGBoost model to predict churn and identify churn drivers.
* Designed a 3-page Power BI dashboard with executive, operational, and account-level views.
* Built a retention action queue and Customer 360 profile for customer success teams.

---

## Final Outcome

This project demonstrates how a modern data analyst can combine Python, BigQuery, SQL, machine learning, and Power BI to build an enterprise-style SaaS churn intelligence solution.

The final dashboard helps executives monitor churn movement, quantify MRR exposure, and guide customer success teams toward the accounts most likely to benefit from retention action.
