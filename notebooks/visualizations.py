import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Saves charts as files instead of popup windows
import seaborn as sns
import os

# ── SETUP ─────────────────────────────────────────────────────
conn = sqlite3.connect('/Users/virajpatel/Churn_Analytics_Project/data/churn_analysis.db')
df = pd.read_sql("SELECT * FROM telco_churn", conn)
conn.close()

# Fix TotalCharges column (has spaces, should be numeric)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)

output_dir = '/Users/virajpatel/Desktop/churn_analytics_project/outputs'
os.makedirs(output_dir, exist_ok=True)

sns.set_theme(style="whitegrid")
colors = ['#2ecc71', '#e74c3c']

print("Generating charts...")

# ── CHART 1: Overall Churn Rate (Pie Chart) ───────────────────
fig, ax = plt.subplots(figsize=(7, 7))
churn_counts = df['Churn'].value_counts()
ax.pie(churn_counts, labels=['Retained (73.46%)', 'Churned (26.54%)'],
       colors=colors, autopct='%1.1f%%', startangle=90,
       textprops={'fontsize': 13})
ax.set_title('Overall Customer Churn Rate', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{output_dir}/01_overall_churn_rate.png', dpi=150)
plt.close()
print("Chart 1 saved.")

# ── CHART 2: Churn by Contract Type (Bar Chart) ───────────────
fig, ax = plt.subplots(figsize=(9, 6))
contract_churn = df.groupby('Contract')['Churn_Binary'].mean() * 100
contract_churn = contract_churn.sort_values(ascending=False)
bars = ax.bar(contract_churn.index, contract_churn.values,
              color=['#e74c3c', '#e67e22', '#2ecc71'], edgecolor='white')
for bar, val in zip(bars, contract_churn.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Churn Rate by Contract Type', fontsize=16, fontweight='bold')
ax.set_xlabel('Contract Type', fontsize=12)
ax.set_ylabel('Churn Rate (%)', fontsize=12)
ax.set_ylim(0, 55)
plt.tight_layout()
plt.savefig(f'{output_dir}/02_churn_by_contract.png', dpi=150)
plt.close()
print("Chart 2 saved.")

# ── CHART 3: Churn by Tenure Group (Bar Chart) ────────────────
fig, ax = plt.subplots(figsize=(9, 6))
df['tenure_group'] = pd.cut(df['tenure'],
    bins=[0, 12, 24, 48, 100],
    labels=['0-12 months', '13-24 months', '25-48 months', '49+ months'])
tenure_churn = df.groupby('tenure_group', observed=True)['Churn_Binary'].mean() * 100
bars = ax.bar(tenure_churn.index, tenure_churn.values,
              color=['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71'], edgecolor='white')
for bar, val in zip(bars, tenure_churn.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Churn Rate by Customer Tenure', fontsize=16, fontweight='bold')
ax.set_xlabel('Tenure Group', fontsize=12)
ax.set_ylabel('Churn Rate (%)', fontsize=12)
ax.set_ylim(0, 60)
plt.tight_layout()
plt.savefig(f'{output_dir}/03_churn_by_tenure.png', dpi=150)
plt.close()
print("Chart 3 saved.")

# ── CHART 4: Revenue at Risk (Bar Chart) ──────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
revenue = df.groupby('Churn')['MonthlyCharges'].sum()
bars = ax.bar(['Retained Customers', 'Churned Customers'],
              revenue.values, color=colors, edgecolor='white')
for bar, val in zip(bars, revenue.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
            f'${val:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Monthly Revenue: Retained vs Churned Customers', fontsize=15, fontweight='bold')
ax.set_ylabel('Total Monthly Revenue ($)', fontsize=12)
ax.set_ylim(0, 380000)
plt.tight_layout()
plt.savefig(f'{output_dir}/04_revenue_at_risk.png', dpi=150)
plt.close()
print("Chart 4 saved.")

# ── CHART 5: Churn by Internet Service ────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
internet_churn = df.groupby('InternetService')['Churn_Binary'].mean() * 100
internet_churn = internet_churn.sort_values(ascending=False)
bars = ax.bar(internet_churn.index, internet_churn.values,
              color=['#e74c3c', '#e67e22', '#2ecc71'], edgecolor='white')
for bar, val in zip(bars, internet_churn.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Churn Rate by Internet Service Type', fontsize=16, fontweight='bold')
ax.set_xlabel('Internet Service', fontsize=12)
ax.set_ylabel('Churn Rate (%)', fontsize=12)
ax.set_ylim(0, 55)
plt.tight_layout()
plt.savefig(f'{output_dir}/05_churn_by_internet.png', dpi=150)
plt.close()
print("Chart 5 saved.")

# ── CHART 6: Monthly Charges Distribution ────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
for churn_val, color, label in zip(['No', 'Yes'], colors, ['Retained', 'Churned']):
    subset = df[df['Churn'] == churn_val]['MonthlyCharges']
    ax.hist(subset, bins=30, alpha=0.6, color=color, label=label, edgecolor='white')
ax.set_title('Monthly Charges Distribution: Retained vs Churned', fontsize=15, fontweight='bold')
ax.set_xlabel('Monthly Charges ($)', fontsize=12)
ax.set_ylabel('Number of Customers', fontsize=12)
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/06_monthly_charges_distribution.png', dpi=150)
plt.close()
print("Chart 6 saved.")

print("\n✅ All 6 charts saved to outputs/ folder")
print(f"Location: {output_dir}")