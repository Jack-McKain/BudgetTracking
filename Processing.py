# app.py
import pandas as pd
import matplotlib.pyplot as plt
import sys

# ---- utility functions from above ----
def load_data(path):
    df = pd.read_csv(path, dtype=str)
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
    df['Debit']  = pd.to_numeric(df['Debit'].str.replace(',', ''), errors='coerce')
    df['Category'] = df['Category'].fillna('Uncategorized')
    return df

def compute_monthly_spending(df):
    df = df.copy()
    df['Month'] = df['Transaction Date'].dt.to_period('M')
    return df.groupby('Month')['Debit'].sum()

def compute_category_monthly(df):
    df = df.copy()
    df['Month'] = df['Transaction Date'].dt.to_period('M')
    return df.groupby(['Month', 'Category'])['Debit'].sum().unstack(fill_value=0)

# ---- main ----
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python app.py path/to/statement.csv")
        sys.exit(1)

    df = load_data(sys.argv[1])

    # Monthly totals
    monthly = compute_monthly_debits(df)
    monthly.plot(kind='bar', figsize=(10,6), color='skyblue')
    plt.title('Monthly Debit Spending')
    plt.ylabel('USD')
    plt.tight_layout()
    plt.show()

    # Category breakdown
    cat_monthly = compute_category_monthly(df)
    cat_monthly.plot(kind='bar', stacked=True, figsize=(12,7), colormap='tab20')
    plt.title('Monthly Spending by Category')
    plt.ylabel('USD')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()