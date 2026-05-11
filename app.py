from config import api_key, pipeline_manifest
from fred_client import fetch_fred_feed, load_to_server

def main():
    for item in pipeline_manifest:
        series_id = item["series_id"]
        table = item["table"]
        col = item["col"]

        data = fetch_fred_feed(api_key=api_key, series_id=series_id)
        if data:
                load_to_server(data=data, table_name=table, value_column_name=col)
        else:
            print("Failed to fetch data from FRED API")

if __name__ == "__main__":
    main()