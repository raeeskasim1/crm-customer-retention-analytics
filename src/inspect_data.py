
from pathlib import Path
import pandas as pd

# Load dataset
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw" / "telco_customer_churn.csv"

df = pd.read_csv(file_path)

# 1. Dataset size
print("\n=== DATASET SHAPE ===")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Preview records
print("\n=== FIRST 5 RECORDS ===")
print(df.head().to_string(index=False))

# 3. Column names and data types
print("\n=== COLUMN INFORMATION ===")
df.info()

# 4. Missing values
print("\n=== MISSING VALUES ===")
print(df.isnull().sum().to_string())

# 5. Empty strings (not detected by isnull)
print("\n=== BLANK STRING COUNTS ===")
for col in df.select_dtypes(include=["object", "string"]).columns:
    blanks = df[col].astype("string").str.strip().eq("").sum()
    if blanks > 0:
        print(f"{col}: {blanks}")

# 6. Duplicate checks
print("\n=== DUPLICATE RECORDS ===")
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate customer IDs:", df["customerID"].duplicated().sum())

# 7. Churn distribution
print("\n=== CHURN DISTRIBUTION ===")
print(df["Churn"].value_counts(dropna=False).to_string())

# 8. Check whether TotalCharges is numeric
print("\n=== TOTAL CHARGES VALIDATION ===")
numeric_charges = pd.to_numeric(df["TotalCharges"], errors="coerce")
print("Non-numeric or missing TotalCharges:", numeric_charges.isna().sum())

print("\nInspection completed successfully.")


print("\n=== BLANK TOTAL CHARGES ===")

blank_customers = df[
    df["TotalCharges"].str.strip() == ""
]

print(
    blank_customers[
        ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]
    ].to_string(index=False)
)

print("\nTenure distribution:")
print(blank_customers["tenure"].value_counts())
