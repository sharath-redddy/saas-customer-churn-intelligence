-- =====================================================
-- 02_create_analytics_table.sql
-- Creates curated analytics table from raw SaaS churn data
-- =====================================================

CREATE OR REPLACE TABLE `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_monthly` AS
SELECT
  company_id,
  billing_month,

  EXTRACT(YEAR FROM billing_month) AS billing_year,
  EXTRACT(MONTH FROM billing_month) AS billing_month_number,
  FORMAT_DATE('%Y-%m', billing_month) AS billing_month_label,

  industry,
  region,
  company_size,
  subscription_tier,
  contract_type,

  seats_purchased,
  active_users,
  support_tickets,
  feature_usage_score,
  account_health_score,
  tenure_months,
  mrr,
  churn,
  customer_status,

  ROUND(SAFE_DIVIDE(active_users, seats_purchased), 4) AS user_adoption_rate,

  CASE
    WHEN account_health_score < 40 THEN 'High Risk'
    WHEN account_health_score BETWEEN 40 AND 69 THEN 'Medium Risk'
    ELSE 'Low Risk'
  END AS health_segment,

  CASE
    WHEN feature_usage_score < 40 AND support_tickets >= 6 THEN 'Low Usage + High Support'
    WHEN feature_usage_score < 40 THEN 'Low Product Usage'
    WHEN support_tickets >= 6 THEN 'High Support Burden'
    ELSE 'Healthy'
  END AS churn_risk_reason,

  CURRENT_TIMESTAMP() AS transformed_at

FROM `sage-momentum-472609-n9.saas_churn_raw.saas_customer_churn_raw`;
