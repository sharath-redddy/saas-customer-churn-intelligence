import warnings
warnings.filterwarnings("ignore")

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_gbq

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier


# ---------------------------------------------------------
# SaaS Customer Churn Prediction Model
# Project: FlowSync CRM - B2B SaaS Churn Analytics
# Warehouse: Google BigQuery
# Model: XGBoost Classifier
# ---------------------------------------------------------

PROJECT_ID = "sage-momentum-472609-n9"

OUTPUT_DIR = Path("outputs")
MODEL_DIR = Path("models")

OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)


def load_data_from_bigquery() -> pd.DataFrame:
    """
    Pull curated monthly churn data from BigQuery.
    """

    query = """
    SELECT
      company_id,
      billing_month,
      billing_year,
      billing_month_number,
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
      user_adoption_rate,
      health_segment,
      churn_risk_reason,
      churn
    FROM `sage-momentum-472609-n9.saas_churn_analytics.customer_churn_monthly`
    """

    print("Loading data from BigQuery...")
    df = pandas_gbq.read_gbq(
        query,
        project_id=PROJECT_ID,
        dialect="standard"
    )

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")
    return df


def prepare_features(df: pd.DataFrame):
    """
    Prepare features and target variable.
    Avoid leakage columns like customer_status.
    Avoid high-cardinality company_id as a model feature.
    """

    df = df.copy()

    # Convert date field
    df["billing_month"] = pd.to_datetime(df["billing_month"])

    # Additional useful time feature
    df["billing_quarter"] = df["billing_month"].dt.quarter

    target_col = "churn"

    numeric_features = [
        "billing_year",
        "billing_month_number",
        "billing_quarter",
        "seats_purchased",
        "active_users",
        "support_tickets",
        "feature_usage_score",
        "account_health_score",
        "tenure_months",
        "mrr",
        "user_adoption_rate"
    ]

    categorical_features = [
        "industry",
        "region",
        "company_size",
        "subscription_tier",
        "contract_type",
        "health_segment",
        "churn_risk_reason"
    ]

    feature_cols = numeric_features + categorical_features

    X = df[feature_cols]
    y = df[target_col].astype(int)

    print("\nTarget distribution:")
    print(y.value_counts(normalize=True).mul(100).round(2).astype(str) + "%")

    # One-hot encode categorical features
    X_encoded = pd.get_dummies(
        X,
        columns=categorical_features,
        drop_first=True
    )

    # Scale numeric features
    scaler = StandardScaler()
    X_encoded[numeric_features] = scaler.fit_transform(X_encoded[numeric_features])

    return X_encoded, y, scaler


def train_model(X: pd.DataFrame, y: pd.Series):
    """
    Train-test split and XGBoost model training.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    negative_count = (y_train == 0).sum()
    positive_count = (y_train == 1).sum()

    scale_pos_weight = negative_count / positive_count

    model = XGBClassifier(
        n_estimators=350,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="binary:logistic",
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        tree_method="hist"
    )

    print("\nTraining XGBoost model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba)
    }

    print("\nModel Performance:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model, X_train, X_test, y_train, y_test, y_pred, y_proba, metrics


def export_outputs(model, X, scaler, metrics):
    """
    Export model, feature importance, metrics, and visual plot.
    """

    # Save model and scaler
    joblib.dump(model, MODEL_DIR / "xgboost_churn_model.pkl")
    joblib.dump(scaler, MODEL_DIR / "feature_scaler.pkl")

    # Save metrics
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)

    # Feature importance
    feature_importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    feature_importance_df.to_csv(
        OUTPUT_DIR / "feature_importance.csv",
        index=False
    )

    print("\nTop 15 Churn Drivers:")
    print(feature_importance_df.head(15))

    # Plot top 15 feature importances
    top_features = feature_importance_df.head(15).sort_values("importance")

    plt.figure(figsize=(10, 7))
    plt.barh(top_features["feature"], top_features["importance"])
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("Top 15 XGBoost Churn Drivers")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_importance_top15.png", dpi=300)
    plt.close()

    print("\nFiles exported:")
    print("models/xgboost_churn_model.pkl")
    print("models/feature_scaler.pkl")
    print("outputs/model_metrics.csv")
    print("outputs/feature_importance.csv")
    print("outputs/feature_importance_top15.png")


def main():
    df = load_data_from_bigquery()
    X, y, scaler = prepare_features(df)
    model, X_train, X_test, y_train, y_test, y_pred, y_proba, metrics = train_model(X, y)
    export_outputs(model, X, scaler, metrics)


if __name__ == "__main__":
    main()