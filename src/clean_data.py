
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data/raw/telco_customer_churn.csv"
output_path = BASE_DIR / "data/processed/telco_cleaned.csv"

# Load dataset
df = pd.read_csv(input_path)

print("Original shape:", df.shape)

# Remove extra spaces from text columns
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].str.strip()

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Check missing values
missing = df["TotalCharges"].isna()

print("Missing TotalCharges:", missing.sum())

# Ensure all missing values belong to zero-tenure customers
if (missing & (df["tenure"] != 0)).any():
    raise ValueError("Unexpected missing TotalCharges detected")

# Mark imputed records
df["TotalChargesImputed"] = missing.astype(int)

# Assumption: zero-tenure customers have no accumulated charges
df.loc[missing, "TotalCharges"] = 0.0

# Check duplicate IDs
if df["customerID"].duplicated().any():
    raise ValueError("Duplicate customer IDs detected")

# Verify cleaning
print("\n=== CLEANING RESULTS ===")
print("Final shape:", df.shape)
print("Missing values:", df.isna().sum().sum())
print("Duplicate customers:", df["customerID"].duplicated().sum())
print("Imputed values:", df["TotalChargesImputed"].sum())
print("TotalCharges dtype:", df["TotalCharges"].dtype)

# Save cleaned data
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("\nCleaned CSV saved:", output_path)
