import psycopg2
import requests
import os
from psycopg2 import sql
from psycopg2.extras import execute_values
from config import api_key, DB_PARAMS

def fetch_fred_feed(api_key, series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "sort_order": "asc",
        "file_type": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            clean_data = []

            for obs in data["observations"]:
                date = obs["date"]
                rate = obs["value"]

                if rate.strip() != ".":
                    clean_data.append((date, float(rate), "FRED")) 
            return clean_data
        
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")

def load_to_server(data, table_name, value_column_name):
    if not data:
        print("No Data")
        return

    query = sql.SQL("""
        INSERT INTO {table} (observation_date, {val_col}, feed_source)
        VALUES %s
        ON CONFLICT (observation_date) DO UPDATE SET 
            {val_col} = EXCLUDED.{val_col},
            pull_date = CURRENT_DATE;
    """).format(
        table=sql.Identifier(table_name),
        val_col=sql.Identifier(value_column_name)
    )

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, query, data)
                print(f"Successfully loaded {len(data)} rows in {table_name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()



