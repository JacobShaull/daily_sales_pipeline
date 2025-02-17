import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("database/sales.db")

### 1️⃣ Total Sales by Product Category (Keep this)
query = """
SELECT product_category, SUM(total_amount) as total_sales
FROM sales_data
GROUP BY product_category
ORDER BY total_sales DESC;
"""
df_total_sales = pd.read_sql(query, conn)
print("\n💵 Total Sales Per Product Category:\n", df_total_sales)

### 2️⃣ Top Selling Products (Keep this)
query = """
SELECT product_category, SUM(quantity) as total_sold
FROM sales_data
GROUP BY product_category
ORDER BY total_sold DESC
LIMIT 5;
"""
df_top_sellers = pd.read_sql(query, conn)
print("\n🏆 Top 5 Selling Products:\n", df_top_sellers)

### 3️⃣ Daily Sales Trends (NEW)
query = """
SELECT date, SUM(total_amount) as total_sales
FROM sales_data
GROUP BY date
ORDER BY date;
"""
df_daily_trends = pd.read_sql(query, conn)
print("\n📈 Daily Sales Trends:\n", df_daily_trends)

### 4️⃣ Gender-Based Purchasing Trends (NEW)
query = """
SELECT gender, product_category, SUM(total_amount) as total_spent
FROM sales_data
GROUP BY gender, product_category
ORDER BY gender, total_spent DESC;

"""
df_gender_spending = pd.read_sql(query, conn)
print("\n👥 Gender-Based Purchasing Trends:\n", df_gender_spending)

### 5️⃣ Sales Distribution by Price Range (NEW)
query = """
SELECT 
    CASE 
        WHEN total_amount < 100 THEN 'Low ($0-$99)'
        WHEN total_amount BETWEEN 100 AND 500 THEN 'Medium ($100-$499)'
        ELSE 'High ($500+)'
    END AS price_range,
    COUNT(*) as transactions
FROM sales_data
GROUP BY price_range
ORDER BY transactions DESC;
"""
df_price_distribution = pd.read_sql(query, conn)
print("\n💰 Sales Distribution by Price Range:\n", df_price_distribution)

query = """
SELECT 
    CASE 
        WHEN age BETWEEN 13 AND 19 THEN 'Teen (13-19)'
        WHEN age BETWEEN 20 AND 29 THEN 'Young Adult (20-29)'
        WHEN age BETWEEN 30 AND 49 THEN 'Adult (30-49)'
        ELSE 'Senior (50+)'
    END as age_group,
    product_category,
    SUM(total_amount) as total_spent
FROM sales_data
GROUP BY age_group, product_category
ORDER BY age_group, total_spent DESC;
"""
df_age_groups = pd.read_sql(query, conn)
print("\n📊 Spending by Age Group:\n", df_age_groups)


# Close connection
conn.close()
