import pandas as pd
import random

# Load original dataset
df = pd.read_csv("data/retail_sales_dataset.csv")

# Ensure column names are lowercase and formatted properly
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Generate new transaction IDs if missing
if "transaction_id" not in df.columns:
    df["transaction_id"] = range(1001, 1001 + len(df))  # Create unique IDs

# Simulate new transactions by increasing transaction IDs
df["transaction_id"] = df["transaction_id"] + random.randint(1000, 9999)

# Save as "new_sales.csv"
df.to_csv("data/new_sales.csv", index=False)

print("✅ New sales data generated!")
