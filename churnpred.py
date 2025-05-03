# === churn_pipeline.py ===
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import roc_auc_score

# 1. Load & label data
df = pd.read_csv("customer_data.csv")
df["churn"] = (df["days_since_last_order"] > 60).astype(int)

# 2. Feature engineering
df["rfm_recency"] = df["days_since_last_order"]
df["rfm_frequency"] = df["total_orders"]
df["rfm_monetary"] = df["total_spend"]

# 3. Preprocessing pipeline
numeric_features = ["rfm_recency", "rfm_frequency", "rfm_monetary", "num_support_tickets"]
categorical_features = ["region", "customer_tier"]
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

# 4. Modeling pipeline with hyperparam tuning
pipeline = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(random_state=42, class_weight="balanced"))
])

param_grid = {
    "clf__n_estimators": [100, 300],
    "clf__max_depth": [5, 10, None]
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = GridSearchCV(pipeline, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1)

# 5. Train & evaluate
X = df[numeric_features + categorical_features]
y = df["churn"]
grid.fit(X, y)

best = grid.best_estimator_
y_pred_proba = best.predict_proba(X)[:, 1]
print("Best ROC AUC:", roc_auc_score(y, y_pred_proba))
print("Best params:", grid.best_params_)

# 6. Save model
import joblib
joblib.dump(best, "churn_model.pkl")

# 7. Inference example
sample = X.sample(3, random_state=0)
print("Sample risk scores:", best.predict_proba(sample)[:, 1])
