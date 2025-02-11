import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# Load and clean data
df = pd.read_csv("data/retail_sales_dataset.csv")
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Check if new sales data exists and append it
try:
    new_df = pd.read_csv("data/new_sales.csv")
    df = pd.concat([df, new_df], ignore_index=True)
    print("✅ New sales data added!")
except FileNotFoundError:
    print("⚠ No new sales data found. Running with existing dataset.")

df['date'] = pd.to_datetime(df['date'])
if 'customer_id' in df.columns:
    df.drop(columns=['customer_id'], inplace=True)
pd.set_option('display.max_columns', None)  # Show all columns when printing

# Save cleaned version
df.to_csv("data/cleaned_retail_sales.csv", index=False)

# Connect to SQLite database
conn = sqlite3.connect("database/sales.db")

# Load existing data from SQLite
existing_data = pd.read_sql("SELECT * FROM sales_data", conn)

# Identify new transactions (rows not already in the database)
new_data = df[~df["transaction_id"].isin(existing_data["transaction_id"])]

# Append only new transactions
new_data.to_sql("sales_data", conn, if_exists="append", index=False)

### **QUERIES FOR INSIGHTS**
# 1️⃣ Show all unique product categories
query = "SELECT DISTINCT product_category FROM sales_data;"
df_categories = pd.read_sql(query, conn)
print("Unique Product Categories:\n", df_categories)

# 2️⃣ Total sales per product category
query = """
SELECT product_category, SUM(total_amount) as total_sales
FROM sales_data
GROUP BY product_category
ORDER BY total_sales DESC;
"""
df_total_sales = pd.read_sql(query, conn)
print("\nTotal Sales Per Product Category:\n", df_total_sales)

# 3️⃣ Top-selling products by quantity
query = """
SELECT product_category, SUM(quantity) as total_sold
FROM sales_data
GROUP BY product_category
ORDER BY total_sold DESC
LIMIT 5;
"""
df_top_sellers = pd.read_sql(query, conn)
print("\nTop 5 Selling Products:\n", df_top_sellers)

# Close connection
conn.close()
