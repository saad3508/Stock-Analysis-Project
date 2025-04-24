import mysql.connector
import pandas as pd
from config import DB_CONFIG
from visualizations import plot_stock_price

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        symbol VARCHAR(10),
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT
    )
    """)

def insert_data(cursor, data):
    for _, row in data.iterrows():
        cursor.execute("""
            INSERT INTO stocks (date, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))

def get_stock_data(symbol, connection, month_year=None):
    if month_year:
        year, month = month_year.split('-')
        query = """
            SELECT date, close FROM stocks
            WHERE symbol = %s AND YEAR(date) = %s AND MONTH(date) = %s
            ORDER BY date
        """
        return pd.read_sql(query, connection, params=(symbol, year, month))
    else:
        query = "SELECT date, close FROM stocks WHERE symbol = %s ORDER BY date"
        return pd.read_sql(query, connection, params=(symbol,))

if __name__ == "__main__":
    conn = connect_db()
    cursor = conn.cursor()

    create_table(cursor)

    # Load and insert CSV data
    df = pd.read_csv("multi_company_stock_data.csv")  # Replace with your actual file
    insert_data(cursor, df)
    conn.commit()

    # User input
    symbol = input("Enter stock symbol to visualize (e.g., AAPL, GOOGL, MSFT): ").upper()
    month_year = input("Enter month and year (YYYY-MM) to filter (or press Enter to skip): ")

    df_stock = get_stock_data(symbol, conn, month_year if month_year else None)

    if not df_stock.empty:
        plot_stock_price(df_stock, symbol)
    else:
        print("No data found for that symbol and date range.")

    cursor.close()
    conn.close()
