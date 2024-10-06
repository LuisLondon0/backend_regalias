import pyodbc
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    try:
        db_host = os.environ.get('R_DB_HOST')
        db_name = os.environ.get('R_DB_NAME')
        db_user = os.environ.get('R_DB_USER')
        db_password = os.environ.get('R_DB_PASSWORD')

        if not all([db_host, db_name, db_user, db_password]):
            logging.error("One or more environment variables required for database connection are missing.")
            return None

        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            f"Server={db_host};"
            f"Database={db_name};"
            f"UID={db_user};"
            f"PWD={db_password};"
        )
        logging.info("Database connection established successfully.")
        return conn
    except pyodbc.Error as e:
        logging.error(f"Connection error: {e}")
        return None

class DatabaseConnection:
    def __enter__(self):
        self.conn = get_db_connection()
        if self.conn is None:
            raise ConnectionError("Failed to establish database connection.")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")