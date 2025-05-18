from datetime import datetime

import pandas as pd
import psycopg2
from config import config


def create_tables(conn):
    cur = conn.cursor()
    
    with open('task4/schema.sql', 'r') as f:
        for query in f.read().split(';'):
            if query.strip():
                cur.execute(query)

    conn.commit()    
    cur.close()


def insert_crypto_info(conn):
    cur = conn.cursor()
    
    df = pd.read_csv("task1/output.csv", index_col=0)
    
    df["AO"] = df["AO"].fillna(0)
    df["AC"] = df["AC"].fillna(0)
    df["MACD"] = df["MACD"].fillna(0)
    df["signal"] = df["signal"].fillna(0)
    df["histogram"] = df["histogram"].fillna(0)
    
    query = """INSERT INTO crypto_tickers(ticker_name) VALUES """
    for ticker in df["ticker"].unique():
        query += f"('{ticker}'), "
    
    query = query[:-2]
    cur.execute(query)
    
    conn.commit()
    
    for ticker in df["ticker"].unique():
        cur.execute(f"""
            SELECT ticker_id 
            FROM crypto_tickers
            WHERE ticker_name = '{ticker}';
        """)
        
        ticker_id = cur.fetchone()[0]
        
        query = """
            INSERT INTO crypto_quotes(
                ticker_id,
                timestamp,
                open_price,
                highest_price,
                lowest_price,
                close_price,
                macd,
                signal,
                AO,
                AC,
                histogram
            ) VALUES 
        """
        
        for item in df[df["ticker"] == ticker].values:
            query += f"""
                (
                    {ticker_id},
                    '{datetime.strptime(item[1], "%Y-%m-%d")}',
                    {item[2]},
                    {item[3]}, {item[4]},
                    {item[5]}, {item[6]}, {item[7]},
                    {item[8]}, {item[9]}, {item[10]}
                ),
            """
        
        query = query.strip()
        query = query[:-1] + ";"

        cur.execute(query)
        
        conn.commit()
        

def insert_invest_info(conn):
    cur = conn.cursor()
    
    df = pd.read_csv("task2/output.csv", index_col=0)

    df["d_close_price"] = df["d_close_price"].fillna(0)
    
    query = """INSERT INTO invest_tickers(ticker_name) VALUES """
    for ticker in df["ticker"].unique():
        query += f"('{ticker}'), "
    
    query = query[:-2]
    cur.execute(query)
    
    conn.commit()
    
    for ticker in df["ticker"].unique():
        cur.execute(f"""
            SELECT ticker_id 
            FROM invest_tickers
            WHERE ticker_name = '{ticker}';
        """)
        
        ticker_id = cur.fetchone()[0]
        
        query = """
            INSERT INTO invest_quotes(
                ticker_id,
                timestamp,
                open_price,
                highest_price,
                lowest_price,
                close_price,
                volume,
                diff_close_prices
            ) VALUES 
        """
        
        for item in df[df["ticker"] == ticker].values:
            query += f"""
                (
                    {ticker_id}, '{datetime.fromtimestamp(item[1])}',
                    {item[2]}, {item[3]}, {item[4]}, {item[5]}, {item[6]},
                    {item[7]}
                ),
            """
        
        query = query.strip()
        query = query[:-1] + ";"

        cur.execute(query)
        
        conn.commit()


conn = psycopg2.connect(
    dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
    host=config.DB_HOST, port=config.DB_PORT
)

create_tables(conn)
insert_crypto_info(conn)
insert_invest_info(conn)

conn.close()