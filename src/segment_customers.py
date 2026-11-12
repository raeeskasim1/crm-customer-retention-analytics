
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "data" / "processed" / "telco_cleaned.csv"
MODEL_FILE = BASE_DIR / "models" / "crm_segmentation_model.joblib"
OUTPUT_CSV = BASE_DIR / "data" / "processed" / "customer_segments.csv"

ADDON_COLUMNS = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]


def main() -> None:
    # 1. Load the original cleaned customer records.
    df = pd.read_csv(INPUT_CSV)
    if df["customerID"].isna().any() or not df["customerID"].is_unique:
        raise ValueError("Customer IDs must be unique and non-missing.")

    # 2. Recreate exactly the same engineered feature used in Colab.
    df["AddOnCount"] = df[ADDON_COLUMNS].eq("Yes").sum(axis=1)

    # 3. Load the fitted preprocessing + K-Means pipeline from Colab.
    # Only load model files you created or otherwise trust.
    model_bundle = joblib.load(MODEL_FILE)
    feature_names = model_bundle["features"]
    pipeline = model_bundle["pipeline"]
    segment_names = model_bundle["segment_names"]

    # 4. Predict clusters WITHOUT fitting a new model.
    clusters = pipeline.predict(df[feature_names])
    result = df[["customerID"]].copy()
    result["Cluster"] = clusters
    result["Segment"] = result["Cluster"].map(segment_names)

    if result["Segment"].isna().any():
        raise ValueError("Some cluster IDs do not have segment names.")

    # 5. Export for Power BI, with one row per customer.
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_CSV, index=False)

    print("=== SEGMENTATION RESULTS ===")
    print("Total customers:", len(result))
    print("Unassigned customers:", result["Segment"].isna().sum())
    print("\nCustomers per segment:")
    print(result["Segment"].value_counts().to_string())
    print("\nSaved:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
