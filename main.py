import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# Load and clean data
df = pd.read_csv("data/retail_sales_dataset.csv")
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['date'] = pd.to_datetime(df['date'])
df.drop(columns=['customer_id'], inplace=True)  # Removing non-essential data
pd.set_option('display.max_columns', None)  # Show all columns when printing

# Save cleaned version
df.to_csv("data/cleaned_retail_sales.csv", index=False)

# Connect to SQLite database
conn = sqlite3.connect("database/sales.db")

# Save DataFrame to SQLite
df.to_sql("sales_data", conn, if_exists="replace", index=False)

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
