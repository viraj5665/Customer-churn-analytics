import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. LOAD CSV ──────────────────────────────────────────
df = pd.read_csv('../data/telco_churn.csv')
print(f"Rows loaded: {len(df)}")
print(df.head())

# ── 2. LOAD INTO SQLITE DATABASE ─────────────────────────
conn = sqlite3.connect('../data/churn_analysis.db')
df.to_sql('telco_churn', conn, if_exists='replace', index=False)
print("\nData loaded into SQLite database successfully.")

# ── 3. VERIFY WITH SQL QUERY ─────────────────────────────
result = pd.read_sql("SELECT COUNT(*) as total_customers FROM telco_churn", conn)
print(f"\nTotal customers in database: {result['total_customers'][0]}")

conn.close()
print("\nSetup complete!")
