
from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

# Load saved model
model_package = joblib.load(
    BASE_DIR / "models" / "crm_churn_model.joblib"
)

model = model_package["pipeline"]
threshold = model_package["threshold"]
features = model_package["features"]

# Load all customers
df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "telco_cleaned.csv"
)

# Generate churn probabilities
probabilities = model.predict_proba(
    df[features]
)[:, 1]

# Convert probabilities to Yes/No
predictions = [
    "Yes" if probability >= threshold else "No"
    for probability in probabilities
]

# Create results
results = pd.DataFrame({
    "customerID": df["customerID"],
    "ChurnProbability": probabilities,
    "PredictedChurn": predictions,
    "ActualChurn": df["Churn"]
})

# Save results without changing original data
output_path = (
    BASE_DIR / "data" / "processed" / "customer_churn_predictions.csv"
)

results.to_csv(output_path, index=False)

# Verify
print("=== CHURN PREDICTION SUMMARY ===")
print("Total customers:", len(results))
print("Unique customers:", results["customerID"].nunique())
print("Threshold:", threshold)

print("\nPredicted churn distribution:")
print(results["PredictedChurn"].value_counts())

print("\nFirst five predictions:")
print(results.head().to_string(index=False))

print("\nSaved to:", output_path)
