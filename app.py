from flask import Flask, render_template
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend before importing pyplot
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to fetch data from SQLite
def get_sales_data():
    conn = sqlite3.connect("database/sales.db")
    query = """
    SELECT product_category, SUM(total_amount) as total_sales
    FROM sales_data
    GROUP BY product_category
    ORDER BY total_sales DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Generate a bar chart
def generate_chart():
    import matplotlib.pyplot as plt  # Import inside the function to prevent issues
    plt.switch_backend('Agg')  # Force non-GUI backend here
    df = get_sales_data()
    plt.figure(figsize=(6,4))
    plt.bar(df["product_category"], df["total_sales"], color=["blue", "green", "red"])
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales ($)")
    plt.title("Total Sales by Product Category")
    plt.savefig("static/sales_chart.png")
    plt.close()

@app.route("/")
def index():
    generate_chart()  # Generate chart before rendering page
    df = get_sales_data()
    return render_template("index.html", tables=[df.to_html(classes="data")], titles=df.columns.values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
