
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "database/crm.db"
# sql_path = BASE_DIR / "sql/business_queries.sql"
# sql_path = BASE_DIR / "sql/churn_by_tenure.sql"
# sql_path = BASE_DIR / "sql/churn_contract_tenure.sql"
# sql_path = BASE_DIR / "sql/churn_by_internet.sql"
# sql_path = BASE_DIR / "sql/churn_by_monthly_charge.sql"
sql_path = BASE_DIR / "sql/crm_overview.sql"

# Read SQL query
query = sql_path.read_text(encoding="utf-8")

# Connect and execute
with sqlite3.connect(db_path) as conn:
    result = pd.read_sql_query(query, conn)

# print("\n=== CHURN ANALYSIS BY CONTRACT ===")
# print("\n=== CHURN BY CONTRACT AND TENURE ===")
# print("\n=== CHURN BY INTERNET SERVICE ===")
# print("\n=== CHURN BY MONTHLY CHARGES ===")
print("\n=== CRM KPI OVERVIEW ===")
print(result.to_string(index=False))
