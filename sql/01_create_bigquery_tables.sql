-- =====================================================
-- 01_create_bigquery_tables.sql
-- Project: SaaS Customer Churn Intelligence
-- Platform: Google BigQuery
-- Author: Sharath Reddy
-- =====================================================

-- Create datasets
CREATE SCHEMA IF NOT EXISTS `sage-momentum-472609-n9.saas_churn_raw`
OPTIONS (
  location = "US"
);

CREATE SCHEMA IF NOT EXISTS `sage-momentum-472609-n9.saas_churn_analytics`
OPTIONS (
  location = "US"
);

CREATE SCHEMA IF NOT EXISTS `sage-momentum-472609-n9.saas_churn_ml`
OPTIONS (
  location = "US"
);

-- Create raw customer churn table
CREATE OR REPLACE TABLE `sage-momentum-472609-n9.saas_churn_raw.saas_customer_churn_raw` (
  company_id STRING,
  billing_month DATE,
  industry STRING,
  region STRING,
  company_size STRING,
  subscription_tier STRING,
  contract_type STRING,
  seats_purchased INT64,
  active_users INT64,
  support_tickets INT64,
  feature_usage_score INT64,
  account_health_score INT64,
  tenure_months INT64,
  mrr NUMERIC,
  churn INT64,
  customer_status STRING
);
