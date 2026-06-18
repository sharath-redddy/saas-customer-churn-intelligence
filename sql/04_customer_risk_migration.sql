-- =====================================================
-- 04_customer_risk_migration.sql
-- Creates customer-level risk migration table
-- Purpose: Track customer movement across risk bands month-over-month
-- =====================================================

CREATE OR REPLACE TABLE `sage-momentum-472609-n9.saas_churn_analytics.customer_risk_migration` AS
WITH source_data AS (
  SELECT
    company_id,
    billing_month,
    billing_month_label,
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
    mrr AS current_mrr,
    churn,
    customer_status,
    churn_risk_reason,
    risk_band AS current_risk_band,
    churn_risk_score AS current_risk_score,

    CASE
      WHEN risk_band = 'Low Risk' THEN 1
      WHEN risk_band = 'Medium Risk' THEN 2
      WHEN risk_band = 'High Risk' THEN 3
      WHEN risk_band = 'Critical Risk' THEN 4
      ELSE 0
    END AS current_risk_rank

  FROM `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_risk_scores`
),

migration_base AS (
  SELECT
    *,
    LAG(current_risk_band) OVER (
      PARTITION BY company_id
      ORDER BY billing_month
    ) AS previous_risk_band,

    LAG(current_risk_score) OVER (
      PARTITION BY company_id
      ORDER BY billing_month
    ) AS previous_risk_score,

    LAG(current_risk_rank) OVER (
      PARTITION BY company_id
      ORDER BY billing_month
    ) AS previous_risk_rank,

    LAG(current_mrr) OVER (
      PARTITION BY company_id
      ORDER BY billing_month
    ) AS previous_mrr

  FROM source_data
),

latest_month AS (
  SELECT MAX(billing_month) AS max_billing_month
  FROM source_data
),

final AS (
  SELECT
    m.company_id,
    m.billing_month,
    m.billing_month_label,
    m.industry,
    m.region,
    m.company_size,
    m.subscription_tier,
    m.contract_type,
    m.seats_purchased,
    m.active_users,
    m.support_tickets,
    m.feature_usage_score,
    m.account_health_score,
    m.tenure_months,
    m.current_mrr,
    m.previous_mrr,
    ROUND(m.current_mrr - COALESCE(m.previous_mrr, 0), 2) AS mrr_change,
    m.churn,
    m.customer_status,
    m.churn_risk_reason,

    m.previous_risk_band,
    m.current_risk_band,
    m.previous_risk_score,
    m.current_risk_score,
    m.previous_risk_rank,
    m.current_risk_rank,

    CASE
      WHEN m.previous_risk_rank IS NULL THEN 'New / No Previous Month'
      WHEN m.current_risk_rank > m.previous_risk_rank THEN 'Worsened'
      WHEN m.current_risk_rank < m.previous_risk_rank THEN 'Improved'
      ELSE 'Stable'
    END AS risk_movement,

    CONCAT(
      COALESCE(m.previous_risk_band, 'No Previous'),
      ' → ',
      m.current_risk_band
    ) AS migration_path,

    CASE
      WHEN m.billing_month = lm.max_billing_month THEN TRUE
      ELSE FALSE
    END AS is_latest_month

  FROM migration_base m
  CROSS JOIN latest_month lm
)

SELECT
  *,
  REPLACE(migration_path, ' Risk', '') AS short_migration_path

FROM final;
