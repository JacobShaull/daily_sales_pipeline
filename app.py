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
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
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
        conn.commit()
        conn.close()

ensure_database()

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

# Flask route to render dashboard
@app.route("/")
def index():
    generate_chart()  # Ensure chart is generated before page loads
    generate_gender_chart()  # Generate gender spending chart
    df = get_sales_data()
    return render_template("index.html", tables=[df.to_html(classes="data")], titles=df.columns.values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
