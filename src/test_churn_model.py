
from pathlib import Path
import joblib
import pandas as pd

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load saved model package
model_path = BASE_DIR / "models" / "crm_churn_model.joblib"
model_package = joblib.load(model_path)

model = model_package["pipeline"]
threshold = model_package["threshold"]
features = model_package["features"]

print("Model loaded successfully!")
print("Model:", model_package["model_name"])
print("Threshold:", threshold)

# Load customer data
data_path = BASE_DIR / "data" / "processed" / "telco_cleaned.csv"
df = pd.read_csv(data_path)

# Select five sample customers
sample = df.head(5).copy()
X_sample = sample[features]

# Predict churn probability
probabilities = model.predict_proba(X_sample)[:, 1]

# Apply selected threshold
predictions = (probabilities >= threshold).astype(int)

# Show results
results = pd.DataFrame({
    "CustomerID": sample["customerID"].values,
    "Churn Probability": probabilities.round(4),
    "Predicted Churn": [
        "Yes" if p == 1 else "No"
        for p in predictions
    ],
    "Actual Churn": sample["Churn"].values
})

print("\n=== CUSTOMER CHURN PREDICTIONS ===")
print(results.to_string(index=False))
