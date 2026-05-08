import psycopg2
import requests
import os
from psycopg2.extras import execute_values
from config import api_key, DB_PARAMS

def fetch_sofr(api_key, start_date = "2018-04-03"):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "SOFR",
        "api_key": api_key,
        "sort_order": "asc",
        "file_type": "json",
        "observation_start": start_date
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

def fetch_10Y(api_key):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "DGS10",
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

def fetch_2Y(api_key):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "DGS2",
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

def load_to_server(data):
    if not data:
        print("No Data")
        return

    query = """
        INSERT INTO fact_sofr_rates(observation_date, sofr_value, feed_source)
        VALUES %s
        ON CONFLICT (observation_date) DO UPDATE SET
            sofr_value = EXCLUDED.sofr_value,
            pull_date = CURRENT_DATE;
    """

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, query, data)
                print(f"Successfully loaded {len(data)} rows.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

# SOFR started trading on 2018-04-03
data = fetch_sofr(api_key=api_key, start_date="2018-04-03")
if data:
    load_to_server(data)
else:
    print("Failed to fetch data from FRED API")
#today_str = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')

