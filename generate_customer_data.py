# generate_customer_data.py
import numpy as np
import pandas as pd

# Seed for reproducibility
np.random.seed(42)

N = 1000

# Recency: days since last order, skewed towards recent activity
days_since_last_order = np.random.exponential(scale=30, size=N).astype(int)

# Frequency: total orders in the past year, between 1–50
total_orders = np.random.poisson(lam=5, size=N) + 1

# Monetary: total spend in USD, correlated with frequency
total_spend = (total_orders * np.random.uniform(20, 200, size=N)).round(2)

# Support tickets: 0–10, skewed towards 0
num_support_tickets = np.random.poisson(lam=1, size=N)

# Region: sample from three regions
regions = np.random.choice(["East", "West", "Central"], size=N, p=[0.5, 0.3, 0.2])

# Customer tier: Bronze/Silver/Gold
tiers = np.random.choice(["Bronze", "Silver", "Gold"], size=N, p=[0.6, 0.3, 0.1])

# Build DataFrame
df = pd.DataFrame({
    "days_since_last_order": days_since_last_order,
    "total_orders": total_orders,
    "total_spend": total_spend,
    "num_support_tickets": num_support_tickets,
    "region": regions,
    "customer_tier": tiers
})

# Save to CSV
df.to_csv("customer_data.csv", index=False)
print("✔️ Generated customer_data.csv with", len(df), "rows")
