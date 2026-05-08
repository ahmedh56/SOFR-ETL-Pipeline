import psycopg2
from config import DB_PARAMS

def connection_test():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        print("Successfully Connnected to DB")
        conn.close()
        return True
    except Exception as e:
        print(f"Conncetion Failed!: {e}")
        return False
    
def db_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        print("Successfully Connnected to DB")
        return conn
    except Exception as e:
        print(f"Conncetion Failed!: {e}")
        return None
