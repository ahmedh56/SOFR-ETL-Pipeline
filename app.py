from config import api_key
from fred_client import fetch_sofr, load_to_server


data = fetch_sofr(api_key=api_key, start_date="2018-04-03")
if data:
    load_to_server(data)
else:
    print("Failed to fetch data from FRED API")