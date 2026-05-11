import os
from dotenv import load_dotenv

# This searches for a .env file and loads the variables
load_dotenv()

api_key = os.getenv("FRED_API_KEY")

if api_key:
    print(f"Key loaded successfully: {api_key[:5]}...") # Just print the start for safety
else:
    print('API Key Not Found')

DB_PARAMS = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

pipeline_manifest = [
    {
        "series_id": "SOFR", 
        "table": "fact_sofr_rates", 
        "col": "sofr_value"
    },
    {
        "series_id": "DGS10", 
        "table": "fact_10yr_treasury_rates", 
        "col": "yield_value"
    },
    {
        "series_id": "DGS2", 
        "table": "fact_2yr_treasury_rates", 
        "col": "yield_value"
    }
]

