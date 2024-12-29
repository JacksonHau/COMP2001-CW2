import pyodbc

def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=DIST-6-505;DATABASE=COMP2001_JHau;UID=JHau;PWD=FxuM888+',
            autocommit=True
        )
        print("Database connection successful!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_db_connection(conn):
    if conn:
        conn.close()
        print("Database connection closed.")
