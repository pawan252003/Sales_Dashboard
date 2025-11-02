from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Prevent GUI issues
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Load dataset
DATA_PATH = "data/SampleSuperstore.csv"
df = pd.read_csv(DATA_PATH, encoding='latin1', on_bad_lines='skip')

# Clean data
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Summary Stats
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df.shape[0]
top_category = df.groupby('Category')['Sales'].sum().idxmax()

# Visualization Function
def create_sales_by_region_chart():
    plt.figure(figsize=(7,4))
    sns.barplot(x='Region', y='Sales', data=df, palette='Blues_d')
    plt.title('Sales by Region', fontsize=14)
    plt.tight_layout()
    chart_path = os.path.join('static', 'sales_by_region.png')
    plt.savefig(chart_path)
    plt.close()

def create_profit_by_category_chart():
    plt.figure(figsize=(7,4))
    sns.barplot(x='Category', y='Profit', data=df, palette='Greens_d')
    plt.title('Profit by Category', fontsize=14)
    plt.tight_layout()
    chart_path = os.path.join('static', 'profit_by_category.png')
    plt.savefig(chart_path)
    plt.close()

@app.route('/')
def index():
    create_sales_by_region_chart()
    create_profit_by_category_chart()

    return render_template('index.html',
                           total_sales=round(total_sales,2),
                           total_profit=round(total_profit,2),
                           total_orders=total_orders,
                           top_category=top_category)

if __name__ == '__main__':
    app.run(debug=True)
