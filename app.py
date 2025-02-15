from flask import Flask, render_template
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Get the absolute path for SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "sales.db")

# Ensure database directory exists
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

# Ensure database exists
def ensure_database():
    """Ensure the database and sales_data table exist, and populate if missing."""
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_data (
        transaction_id INTEGER PRIMARY KEY,
        date TEXT,
        gender TEXT,
        age INTEGER,
        product_category TEXT,
        quantity INTEGER,
        price_per_unit INTEGER,
        total_amount INTEGER
    )
    """)

    # Check if data exists
    cursor.execute("SELECT COUNT(*) FROM sales_data")
    row_count = cursor.fetchone()[0]

    # If empty, load initial data
    if row_count == 0:
        print("⚠ Database is empty. Loading initial data...")
        df = pd.read_csv("data/cleaned_retail_sales.csv")  # Use your cleaned dataset
        df.to_sql("sales_data", conn, if_exists="replace", index=False)
        print("✅ Data successfully loaded into SQLite!")

    conn.commit()
    conn.close()

# Fetch sales data
def get_sales_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT product_category, SUM(total_amount) as total_sales
    FROM sales_data
    GROUP BY product_category
    ORDER BY total_sales DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch gender-based sales data
def get_gender_spending():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT gender, product_category, SUM(total_amount) as total_spent
    FROM sales_data
    GROUP BY gender, product_category
    ORDER BY gender, total_spent DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ✅ **Fixed `get_age_group_spending()`**
def get_age_group_spending():
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()  # Close DB connection
    return df_age_groups  # ✅ Fixed missing return statement

# Generate total sales chart
def generate_chart():
    df = get_sales_data()
    plt.figure(figsize=(6,4))
    plt.bar(df["product_category"], df["total_sales"], color=["blue", "green", "red"])
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales ($)")
    plt.title("Total Sales by Product Category")
    plt.savefig("static/sales_chart.png")
    plt.close()

# Generate gender-based spending chart
def generate_gender_chart():
    df_gender = get_gender_spending()
    plt.figure(figsize=(6,4))
    categories = df_gender["product_category"].unique()

    female_spending = df_gender[df_gender["gender"] == "Female"]["total_spent"].tolist()
    male_spending = df_gender[df_gender["gender"] == "Male"]["total_spent"].tolist()

    x = range(len(categories))
    plt.bar(x, female_spending, width=0.4, label="Female", color="pink", align='center')
    plt.bar(x, male_spending, width=0.4, label="Male", color="blue", align='edge')

    plt.xticks(x, categories)
    plt.xlabel("Product Category")
    plt.ylabel("Total Spent ($)")
    plt.title("Spending by Gender per Category")
    plt.legend()
    plt.savefig("static/gender_chart.png")
    plt.close()

# ✅ **Fixed generate_age_chart()**
def generate_age_chart():
    df_age = get_age_group_spending()
    plt.figure(figsize=(8,6))

    for category in df_age["product_category"].unique():
        subset = df_age[df_age["product_category"] == category]
        plt.bar(subset["age_group"], subset["total_spent"], label=category)

    plt.xlabel("Age Group")
    plt.ylabel("Total Spent ($)")
    plt.title("Spending by Age Group and Product")
    plt.legend()
    plt.savefig("static/age_chart.png")
    plt.close()

# Flask route to render dashboard
@app.route("/")
def index():
    generate_chart()  # Ensure chart is generated before page loads
    generate_gender_chart()  # Generate gender spending chart
    generate_age_chart()  # ✅ Ensure age chart is generated too
    df = get_sales_data()
    return render_template("index.html", tables=[df.to_html(classes="data")], titles=df.columns.values)

# Ensure database is ready before starting Flask app
ensure_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
