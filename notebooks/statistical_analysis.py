import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os

# ── SETUP ─────────────────────────────────────────────────────
conn = sqlite3.connect('/Users/virajpatel/Churn_Analytics_Project/data/churn_analysis.db')
df = pd.read_sql("SELECT * FROM telco_churn", conn)
conn.close()

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)

output_dir = '/Users/virajpatel/Desktop/churn_analytics_project/outputs'
os.makedirs(output_dir, exist_ok=True)

sns.set_theme(style="whitegrid")

print("=" * 60)
print("STATISTICAL ANALYSIS")
print("=" * 60)

# ── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────
print("\n1. DESCRIPTIVE STATISTICS BY CHURN STATUS")
desc = df.groupby('Churn')[['tenure', 'MonthlyCharges', 'TotalCharges']].describe().round(2)
print(desc)

# ── 2. CORRELATION ANALYSIS ───────────────────────────────────
print("\n2. CORRELATION WITH CHURN")
numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
correlations = df[numeric_cols + ['Churn_Binary']].corr()['Churn_Binary'].drop('Churn_Binary').round(4)
print(correlations.sort_values())

# ── 3. HYPOTHESIS TEST ────────────────────────────────────────
print("\n3. HYPOTHESIS TESTING")
print("Are monthly charges significantly different between churned and retained customers?")
churned = df[df['Churn'] == 'Yes']['MonthlyCharges']
retained = df[df['Churn'] == 'No']['MonthlyCharges']
t_stat, p_value = stats.ttest_ind(churned, retained)
print(f"   Churned avg monthly charge:  ${churned.mean():.2f}")
print(f"   Retained avg monthly charge: ${retained.mean():.2f}")
print(f"   T-statistic: {t_stat:.4f}")
print(f"   P-value: {p_value:.6f}")
if p_value < 0.05:
    print("   Result: SIGNIFICANT difference (p < 0.05)")
    print("   Churned customers pay significantly more per month")
else:
    print("   Result: No significant difference")

# ── 4. COHORT ANALYSIS ────────────────────────────────────────
print("\n4. COHORT ANALYSIS — Churn Rate by Tenure + Contract")
df['tenure_group'] = pd.cut(df['tenure'],
    bins=[0, 12, 24, 48, 100],
    labels=['0-12 mo', '13-24 mo', '25-48 mo', '49+ mo'])

cohort = df.groupby(['tenure_group', 'Contract'], observed=True)['Churn_Binary'].mean() * 100
cohort = cohort.round(2).reset_index()
cohort.columns = ['Tenure Group', 'Contract', 'Churn Rate %']
print(cohort.to_string(index=False))

# ── 5. SENIOR CITIZEN ANALYSIS ────────────────────────────────
print("\n5. SENIOR CITIZEN CHURN ANALYSIS")
senior = df.groupby('SeniorCitizen')['Churn_Binary'].agg(['mean', 'count']).round(4)
senior['churn_rate_pct'] = (senior['mean'] * 100).round(2)
senior.index = ['Non-Senior', 'Senior']
print(senior[['count', 'churn_rate_pct']])

# ── 6. CORRELATION HEATMAP ────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
corr_matrix = df[numeric_cols + ['Churn_Binary']].corr().round(2)
sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0,
            fmt='.2f', linewidths=0.5, ax=ax)
ax.set_title('Correlation Heatmap — Churn Drivers', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/07_correlation_heatmap.png', dpi=150)
plt.close()
print("\nChart 7 saved — Correlation Heatmap")

# ── 7. COHORT HEATMAP ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
cohort_pivot = cohort.pivot(index='Tenure Group', columns='Contract', values='Churn Rate %')
sns.heatmap(cohort_pivot, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Churn Rate %'})
ax.set_title('Churn Rate % by Tenure Group and Contract Type', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/08_cohort_heatmap.png', dpi=150)
plt.close()
print("Chart 8 saved — Cohort Heatmap")

# ── 8. KEY FINDINGS SUMMARY ───────────────────────────────────
print("\n" + "=" * 60)
print("KEY FINDINGS SUMMARY")
print("=" * 60)
print(f"""
1. Overall churn rate: 26.54% (1,869 of 7,043 customers)
2. Month-to-month contracts churn 15x more than two-year (42.71% vs 2.83%)
3. Fiber optic customers churn at 41.89% vs 7.40% for no internet
4. New customers (0-12 months) churn at 47.44% — highest risk group
5. Monthly revenue at risk from churned customers: $139,130/month
6. Electronic check users churn at 45.29% vs 15.24% for credit card
7. Churned customers pay ${churned.mean():.2f}/mo vs ${retained.mean():.2f}/mo for retained
8. Senior citizens churn at a higher rate than non-seniors
""")
print("=" * 60)
print("STATISTICAL ANALYSIS COMPLETE")
print("=" * 60)