import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("database/sales.db")

### 1️⃣ Total Sales by Product Category
query = """
SELECT product_category, SUM(total_amount) as total_sales
FROM sales_data
GROUP BY product_category
ORDER BY total_sales DESC;
"""
df_total_sales = pd.read_sql(query, conn)
print("\nTotal Sales Per Product Category:\n", df_total_sales)

### 2️⃣ Top 5 Best-Selling Products by Quantity
query = """
SELECT product_category, SUM(quantity) as total_sold
FROM sales_data
GROUP BY product_category
ORDER BY total_sold DESC
LIMIT 5;
"""
df_top_sellers = pd.read_sql(query, conn)
print("\nTop 5 Selling Products:\n", df_top_sellers)

### 3️⃣ Total Transactions in Database
query = """
SELECT COUNT(*) AS total_transactions FROM sales_data;
"""
df_total_transactions = pd.read_sql(query, conn)
print("\nTotal Transactions in Database:\n", df_total_transactions)


### 4️⃣ Sales Trends by Day of the Week
query = """
SELECT strftime('%w', date) AS day_of_week, SUM(total_amount) as total_sales
FROM sales_data
GROUP BY day_of_week
ORDER BY day_of_week;
"""
df_sales_by_day = pd.read_sql(query, conn)
print("\nSales Trends by Day of the Week:\n", df_sales_by_day)

### 5️⃣ Highest Revenue Impact Products
query = """
SELECT product_category, AVG(total_amount) as avg_transaction_value, SUM(total_amount) as total_revenue
FROM sales_data
GROUP BY product_category
ORDER BY total_revenue DESC;
"""
df_revenue_impact = pd.read_sql(query, conn)
print("\nHighest Revenue Impact Products:\n", df_revenue_impact)


# Close connection
conn.close()
