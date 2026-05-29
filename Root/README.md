# Customer Churn & Revenue Analytics

## Project Overview
End-to-end analytics project analyzing customer churn patterns for a telecom company using SQL, Python, and data visualization.

## Key Findings
- Overall churn rate: 26.54% (1,869 of 7,043 customers)
- Month-to-month contracts churn 15x more than two-year contracts (42.71% vs 2.83%)
- New customers (0-12 months) are highest risk at 47.44% churn rate
- $139,130/month in revenue at risk from churned customers
- Churned customers pay significantly more ($74.44/mo vs $61.27/mo, p < 0.001)
- Senior citizens churn at 41.68% vs 23.61% for non-seniors

## Tools Used
- **Python** (Pandas, Matplotlib, Seaborn, SciPy)
- **SQL** (SQLite — joins, aggregations, window functions, subqueries)
- **Statistical Analysis** (t-tests, correlation analysis, cohort analysis)
- **Data Visualization** (8 charts saved as PNG)

## Project Structure
churn_analytics_project/
├── data/telco_churn.csv
├── notebooks/
│   ├── churn_analysis.py
│   ├── sql_analysis.py
│   ├── statistical_analysis.py
│   └── visualizations.py
├── outputs/ [8 PNG charts]
└── README.md

## Dataset
IBM Telco Customer Churn — 7,043 customers, 21 features