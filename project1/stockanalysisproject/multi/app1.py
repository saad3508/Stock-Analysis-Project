import mysql.connector
import pandas as pd
from config import DB_CONFIG
from multi.visualizations1 import plot_multiple_stocks

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

def get_stock_data(symbols, connection):
    placeholders = ', '.join(['%s'] * len(symbols))
    query = f"SELECT date, symbol, close FROM stocks WHERE symbol IN ({placeholders}) ORDER BY date"
    return pd.read_sql(query, connection, params=tuple(symbols))

if __name__ == "__main__":
    conn = connect_db()
    cursor = conn.cursor()

    create_table(cursor)

    df = pd.read_csv("multi_company_stock_data.csv")  # Updated CSV
    insert_data(cursor, df)
    conn.commit()

    # Input multiple symbols
    symbols_input = input("Enter stock symbols to visualize (comma-separated, e.g., AAPL, MSFT): ")
    symbols = [s.strip().upper() for s in symbols_input.split(",")]

    df_stocks = get_stock_data(symbols, conn)
    if not df_stocks.empty:
        plot_multiple_stocks(df_stocks, symbols)
    else:
        print("No data found for the given symbols.")

    cursor.close()
    conn.close()
