
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "data/processed/telco_cleaned.csv"
db_path = BASE_DIR / "database/crm.db"

df = pd.read_csv(csv_path)

# Connect to SQLite
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON")

# Rebuild tables for repeatable development
conn.executescript("""
DROP TABLE IF EXISTS Billing;
DROP TABLE IF EXISTS Contracts;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,
    Partner TEXT,
    Dependents TEXT,
    tenure INTEGER,
    Churn TEXT
);

CREATE TABLE Services (
    customerID TEXT PRIMARY KEY,
    PhoneService TEXT,
    MultipleLines TEXT,
    InternetService TEXT,
    OnlineSecurity TEXT,
    OnlineBackup TEXT,
    DeviceProtection TEXT,
    TechSupport TEXT,
    StreamingTV TEXT,
    StreamingMovies TEXT,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

CREATE TABLE Contracts (
    customerID TEXT PRIMARY KEY,
    Contract TEXT,
    PaperlessBilling TEXT,
    PaymentMethod TEXT,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

CREATE TABLE Billing (
    customerID TEXT PRIMARY KEY,
    MonthlyCharges REAL,
    TotalCharges REAL,
    TotalChargesImputed INTEGER,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);
""")

# Define columns for each table
tables = {
    "Customers": [
        "customerID", "gender", "SeniorCitizen",
        "Partner", "Dependents", "tenure", "Churn"
    ],
    "Services": [
        "customerID", "PhoneService", "MultipleLines",
        "InternetService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ],
    "Contracts": [
        "customerID", "Contract",
        "PaperlessBilling", "PaymentMethod"
    ],
    "Billing": [
        "customerID", "MonthlyCharges",
        "TotalCharges", "TotalChargesImputed"
    ]
}

# Insert customer data into the related tables
for table_name, columns in tables.items():
    df[columns].to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(f"{table_name}: {count} records")

# Validate foreign key relationships
errors = conn.execute("PRAGMA foreign_key_check").fetchall()

print("Foreign key errors:", len(errors))

conn.commit()
conn.close()

print("\nCRM database created successfully!")
print("Database location:", db_path)
