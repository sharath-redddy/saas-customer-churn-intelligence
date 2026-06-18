-- =====================================================
-- 03_churn_metrics_and_risk_scores.sql
-- Creates SaaS churn analytics views and risk scoring table
-- =====================================================

-- Monthly churn rate
CREATE OR REPLACE VIEW `sage-momentum-472609-n9.saas_churn_analytics.v_monthly_churn_rate` AS
SELECT
  billing_month,
  billing_month_label,

  COUNT(DISTINCT company_id) AS total_customer_records,

  COUNT(DISTINCT CASE 
    WHEN churn = 1 THEN company_id 
  END) AS churned_customers,

  ROUND(
    SAFE_DIVIDE(
      COUNT(DISTINCT CASE WHEN churn = 1 THEN company_id END),
      COUNT(DISTINCT company_id)
    ) * 100,
    2
  ) AS monthly_churn_rate_percent,

  ROUND(SUM(mrr), 2) AS total_mrr

FROM `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_monthly`
GROUP BY
  billing_month,
  billing_month_label;


-- MRR churn
CREATE OR REPLACE VIEW `sage-momentum-472609-n9.saas_churn_analytics.v_mrr_churn` AS
SELECT
  billing_month,
  billing_month_label,

  ROUND(SUM(mrr), 2) AS total_mrr,

  ROUND(SUM(CASE 
    WHEN churn = 1 THEN mrr 
    ELSE 0 
  END), 2) AS churned_mrr,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN churn = 1 THEN mrr ELSE 0 END),
      SUM(mrr)
    ) * 100,
    2
  ) AS mrr_churn_rate_percent,

  COUNT(DISTINCT CASE 
    WHEN churn = 1 THEN company_id 
  END) AS churned_customers

FROM `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_monthly`
GROUP BY
  billing_month,
  billing_month_label;


-- User engagement cohorts
CREATE OR REPLACE VIEW `sage-momentum-472609-n9.saas_churn_analytics.v_user_engagement_cohorts` AS
SELECT
  billing_month,
  billing_month_label,

  CASE
    WHEN feature_usage_score >= 75 THEN 'High Engagement'
    WHEN feature_usage_score BETWEEN 45 AND 74 THEN 'Medium Engagement'
    ELSE 'Low Engagement'
  END AS engagement_cohort,

  CASE
    WHEN user_adoption_rate >= 0.75 THEN 'High Adoption'
    WHEN user_adoption_rate BETWEEN 0.45 AND 0.74 THEN 'Medium Adoption'
    ELSE 'Low Adoption'
  END AS adoption_cohort,

  COUNT(DISTINCT company_id) AS customers,

  ROUND(AVG(feature_usage_score), 2) AS avg_feature_usage_score,
  ROUND(AVG(user_adoption_rate) * 100, 2) AS avg_user_adoption_percent,
  ROUND(AVG(support_tickets), 2) AS avg_support_tickets,

  ROUND(AVG(churn) * 100, 2) AS churn_rate_percent,

  ROUND(SUM(mrr), 2) AS total_mrr,
  ROUND(SUM(CASE WHEN churn = 1 THEN mrr ELSE 0 END), 2) AS churned_mrr

FROM `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_monthly`
GROUP BY
  billing_month,
  billing_month_label,
  engagement_cohort,
  adoption_cohort;


-- Customer churn risk scoring table
CREATE OR REPLACE TABLE `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_risk_scores` AS
WITH base AS (
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
    ROUND(user_adoption_rate * 100, 2) AS user_adoption_percent,

    support_tickets,
    feature_usage_score,
    account_health_score,
    tenure_months,
    mrr,
    churn,
    customer_status,
    churn_risk_reason,

    (
      CASE
        WHEN feature_usage_score < 40 THEN 25 ELSE 0
      END
      +
      CASE
        WHEN support_tickets >= 8 THEN 25
        WHEN support_tickets BETWEEN 5 AND 7 THEN 15
        ELSE 0
      END
      +
      CASE
        WHEN user_adoption_rate < 0.45 THEN 20
        WHEN user_adoption_rate BETWEEN 0.45 AND 0.60 THEN 10
        ELSE 0
      END
      +
      CASE
        WHEN contract_type = 'Monthly' THEN 15 ELSE 0
      END
      +
      CASE
        WHEN account_health_score < 40 THEN 15
        WHEN account_health_score BETWEEN 40 AND 60 THEN 8
        ELSE 0
      END
    ) AS churn_risk_score

  FROM `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_monthly`
)

SELECT
  *,
  CASE
    WHEN churn_risk_score >= 70 THEN 'Critical Risk'
    WHEN churn_risk_score BETWEEN 40 AND 69 THEN 'High Risk'
    WHEN churn_risk_score BETWEEN 20 AND 39 THEN 'Medium Risk'
    ELSE 'Low Risk'
  END AS risk_band

FROM base;
