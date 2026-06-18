import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------
# SaaS Customer Churn Synthetic Dataset Generator
# Project: FlowSync CRM - B2B SaaS Churn Analytics
# Author: Sharath Reddy
# ---------------------------------------------------------

np.random.seed(42)

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

N_COMPANIES = 3000
START_DATE = "2024-01-01"
N_MONTHS = 18

months = pd.date_range(start=START_DATE, periods=N_MONTHS, freq="MS")


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


industries = [
    "Technology",
    "Finance",
    "Healthcare",
    "Retail",
    "Manufacturing",
    "Education",
    "Professional Services",
    "Logistics"
]

regions = [
    "North America",
    "Europe",
    "Asia Pacific",
    "Latin America",
    "Middle East & Africa"
]

company_sizes = ["Small Business", "Mid Market", "Enterprise"]

subscription_tiers = ["Bronze", "Silver", "Gold"]
contract_types = ["Monthly", "Annual"]

tier_base_fee = {
    "Bronze": 300,
    "Silver": 900,
    "Gold": 2200
}

tier_user_fee = {
    "Bronze": 25,
    "Silver": 45,
    "Gold": 80
}

tier_usage_boost = {
    "Bronze": -8,
    "Silver": 3,
    "Gold": 10
}

company_size_user_range = {
    "Small Business": (10, 80),
    "Mid Market": (80, 300),
    "Enterprise": (300, 1000)
}

records = []

for company_num in range(1, N_COMPANIES + 1):
    company_id = f"CUST-{company_num:05d}"

    industry = np.random.choice(industries)
    region = np.random.choice(regions, p=[0.35, 0.25, 0.25, 0.08, 0.07])
    company_size = np.random.choice(company_sizes, p=[0.55, 0.32, 0.13])

    subscription_tier = np.random.choice(
        subscription_tiers,
        p=[0.45, 0.38, 0.17]
    )

    contract_type = np.random.choice(
        contract_types,
        p=[0.58, 0.42]
    )

    min_users, max_users = company_size_user_range[company_size]
    seats_purchased = int(np.random.randint(min_users, max_users))

    base_adoption_rate = np.random.uniform(0.45, 0.95)

    churned = False
    tenure_months = np.random.randint(1, 18)

    for month_index, billing_month in enumerate(months):
        if churned:
            break

        tenure = tenure_months + month_index

        # Product engagement behavior
        seasonality_effect = 4 * np.sin((month_index / 12) * 2 * np.pi)
        usage_noise = np.random.normal(0, 8)

        feature_usage_score = (
            55
            + tier_usage_boost[subscription_tier]
            + seasonality_effect
            + usage_noise
        )

        # Some customers naturally become less engaged over time
        if np.random.random() < 0.12:
            feature_usage_score -= np.random.uniform(10, 25)

        feature_usage_score = int(np.clip(feature_usage_score, 5, 100))

        # Active users depend on seats and product usage
        adoption_rate = base_adoption_rate * (feature_usage_score / 75)
        adoption_rate = np.clip(adoption_rate, 0.10, 1.00)

        active_users = int(seats_purchased * adoption_rate)
        active_users = max(active_users, 1)

        # Support tickets increase when usage is low
        ticket_lambda = 2

        if feature_usage_score < 40:
            ticket_lambda += 5

        if subscription_tier == "Gold":
            ticket_lambda += 2

        if company_size == "Enterprise":
            ticket_lambda += 3

        support_tickets = np.random.poisson(ticket_lambda)

        # MRR calculation
        mrr = (
            tier_base_fee[subscription_tier]
            + active_users * tier_user_fee[subscription_tier]
        )

        # Add realistic revenue noise
        mrr = mrr * np.random.uniform(0.92, 1.08)
        mrr = round(mrr, 2)

        # Account health score
        account_health_score = (
            0.60 * feature_usage_score
            + 0.25 * min((active_users / seats_purchased) * 100, 100)
            - 0.15 * min(support_tickets * 8, 100)
        )

        account_health_score = int(np.clip(account_health_score, 1, 100))

        # Churn probability logic
        monthly_contract_risk = 1 if contract_type == "Monthly" else 0
        bronze_risk = 1 if subscription_tier == "Bronze" else 0
        low_usage_risk = max((55 - feature_usage_score) / 55, 0)
        high_ticket_risk = min(support_tickets / 12, 1)
        low_adoption_risk = 1 if active_users / seats_purchased < 0.45 else 0
        early_tenure_risk = 1 if tenure < 6 else 0

        churn_logit = (
            -3.4
            + 0.85 * monthly_contract_risk
            + 0.45 * bronze_risk
            + 1.35 * low_usage_risk
            + 1.10 * high_ticket_risk
            + 0.75 * low_adoption_risk
            + 0.35 * early_tenure_risk
        )

        churn_probability = sigmoid(churn_logit)

        # Keep churn realistic
        churn_probability = np.clip(churn_probability, 0.01, 0.22)

        churn = np.random.random() < churn_probability

        records.append({
            "company_id": company_id,
            "billing_month": billing_month.strftime("%Y-%m-%d"),
            "industry": industry,
            "region": region,
            "company_size": company_size,
            "subscription_tier": subscription_tier,
            "contract_type": contract_type,
            "seats_purchased": seats_purchased,
            "active_users": active_users,
            "support_tickets": support_tickets,
            "feature_usage_score": feature_usage_score,
            "account_health_score": account_health_score,
            "tenure_months": tenure,
            "mrr": mrr,
            "churn": int(churn)
        })

        if churn:
            churned = True


df = pd.DataFrame(records)

# Add customer status for easier dashboarding
df["customer_status"] = np.where(df["churn"] == 1, "Churned", "Active")

# Reorder columns
df = df[
    [
        "company_id",
        "billing_month",
        "industry",
        "region",
        "company_size",
        "subscription_tier",
        "contract_type",
        "seats_purchased",
        "active_users",
        "support_tickets",
        "feature_usage_score",
        "account_health_score",
        "tenure_months",
        "mrr",
        "churn",
        "customer_status"
    ]
]

output_file = OUTPUT_DIR / "saas_customer_churn.csv"
df.to_csv(output_file, index=False)

print("Synthetic SaaS churn dataset generated successfully.")
print(f"File saved to: {output_file}")
print(f"Total records generated: {len(df):,}")
print(f"Unique companies: {df['company_id'].nunique():,}")
print(f"Date range: {df['billing_month'].min()} to {df['billing_month'].max()}")
print(f"Overall churn rate: {df['churn'].mean() * 100:.2f}%")
print("\nPreview:")
print(df.head(10))