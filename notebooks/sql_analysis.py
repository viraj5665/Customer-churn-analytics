import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('/Users/virajpatel/Churn_Analytics_Project/data/churn_analysis.db')

print("=" * 60)
print("CUSTOMER CHURN SQL ANALYSIS")
print("=" * 60)

# ── QUERY 1: Overall Churn Rate ───────────────────────────────
q1 = pd.read_sql("""
    SELECT 
        Churn,
        COUNT(*) as customer_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM telco_churn), 2) as percentage
    FROM telco_churn
    GROUP BY Churn
""", conn)
print("\n1. OVERALL CHURN RATE")
print(q1.to_string(index=False))

# ── QUERY 2: Churn by Contract Type ──────────────────────────
q2 = pd.read_sql("""
    SELECT 
        Contract,
        COUNT(*) as total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
    FROM telco_churn
    GROUP BY Contract
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n2. CHURN RATE BY CONTRACT TYPE")
print(q2.to_string(index=False))

# ── QUERY 3: Churn by Internet Service ───────────────────────
q3 = pd.read_sql("""
    SELECT 
        InternetService,
        COUNT(*) as total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
    FROM telco_churn
    GROUP BY InternetService
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n3. CHURN RATE BY INTERNET SERVICE")
print(q3.to_string(index=False))

# ── QUERY 4: Churn by Tenure Group ───────────────────────────
q4 = pd.read_sql("""
    SELECT 
        CASE 
            WHEN tenure <= 12 THEN '0-12 months'
            WHEN tenure <= 24 THEN '13-24 months'
            WHEN tenure <= 48 THEN '25-48 months'
            ELSE '49+ months'
        END as tenure_group,
        COUNT(*) as total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
    FROM telco_churn
    GROUP BY tenure_group
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n4. CHURN RATE BY CUSTOMER TENURE")
print(q4.to_string(index=False))

# ── QUERY 5: Revenue at Risk ──────────────────────────────────
q5 = pd.read_sql("""
    SELECT 
        Churn,
        COUNT(*) as customers,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
        ROUND(SUM(MonthlyCharges), 2) as total_monthly_revenue
    FROM telco_churn
    GROUP BY Churn
""", conn)
print("\n5. REVENUE AT RISK FROM CHURNED CUSTOMERS")
print(q5.to_string(index=False))

# ── QUERY 6: High Risk Segments ──────────────────────────────
q6 = pd.read_sql("""
    SELECT 
        Contract,
        InternetService,
        COUNT(*) as customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) as monthly_revenue_lost
    FROM telco_churn
    GROUP BY Contract, InternetService
    HAVING COUNT(*) > 100
    ORDER BY churn_rate_pct DESC
    LIMIT 5
""", conn)
print("\n6. TOP 5 HIGHEST RISK CUSTOMER SEGMENTS")
print(q6.to_string(index=False))

# ── QUERY 7: Payment Method ───────────────────────────────────
q7 = pd.read_sql("""
    SELECT 
        PaymentMethod,
        COUNT(*) as total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
    FROM telco_churn
    GROUP BY PaymentMethod
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n7. CHURN RATE BY PAYMENT METHOD")
print(q7.to_string(index=False))

conn.close()
print("\n" + "=" * 60)
print("SQL ANALYSIS COMPLETE")
print("=" * 60)