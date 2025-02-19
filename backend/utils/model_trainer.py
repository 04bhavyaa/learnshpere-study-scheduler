import numpy as np
import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import StackingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure artifacts directory exists
os.makedirs("artifacts", exist_ok=True)

# Load dataset (replace with your dataset)
df = pd.read_csv("data/cleaned/student-final.csv")

target_column = "G3"

# Define features (X) and target variable (y)
X = df.drop(columns=[target_column])
y = df[target_column]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
linear_model = LinearRegression()
ridge_model = Ridge(alpha=1.0)

# Train models
linear_model.fit(X_train, y_train)
ridge_model.fit(X_train, y_train)

# Predictions
y_pred_linear = linear_model.predict(X_test)
y_pred_ridge = ridge_model.predict(X_test)

# Ensemble (simple average of both models)
y_pred_ensemble = (y_pred_linear + y_pred_ridge) / 2

# Stacking Regressor
stacking_regressor = StackingRegressor(
    estimators=[("linear", linear_model), ("ridge", ridge_model)],
    final_estimator=LinearRegression()
)
stacking_regressor.fit(X_train, y_train)
y_pred_stack = stacking_regressor.predict(X_test)

# Evaluate models
def evaluate(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R²": r2_score(y_true, y_pred)
    }

results = {
    "Linear Regression": evaluate(y_test, y_pred_linear),
    "Ridge Regression": evaluate(y_test, y_pred_ridge),
    "Ensemble (Linear + Ridge)": evaluate(y_test, y_pred_ensemble),
    "Stacking Regressor": evaluate(y_test, y_pred_stack)
}

# Find the best model
best_model_name = max(results, key=lambda k: results[k]["R²"])
best_model = {
    "Linear Regression": linear_model,
    "Ridge Regression": ridge_model,
    "Ensemble (Linear + Ridge)": None,  # No direct model to save
    "Stacking Regressor": stacking_regressor
}[best_model_name]

# Save best model
if best_model is not None:
    joblib.dump(best_model, f"artifacts/best_model.pkl")
    print(f"Best model ({best_model_name}) saved as 'artifacts/best_model.pkl'")
else:
    print(f"Best model is the Ensemble, no direct model file to save.")

# Print results
for model, metrics in results.items():
    print(f"\n{model}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
