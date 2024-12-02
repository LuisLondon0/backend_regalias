from psycopg2 import pool
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabasePool:
    _pool = None

    @staticmethod
    def initialize():
        try:
            DatabasePool._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=2,
                host=os.environ.get('R_DB_HOST'),
                database=os.environ.get('R_DB_NAME'),
                user=os.environ.get('R_DB_USER'),
                password=os.environ.get('R_DB_PASSWORD'),
                port=5432
            )
            logging.info("Database connection pool initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize database connection pool: {e}")
            raise

    @staticmethod
    def get_connection():
        if not DatabasePool._pool:
            raise ConnectionError("Database pool not initialized.")
        return DatabasePool._pool.getconn()

    @staticmethod
    def release_connection(conn):
        if not DatabasePool._pool:
            raise ConnectionError("Database pool not initialized.")
        DatabasePool._pool.putconn(conn)

    @staticmethod
    def close_pool():
        if DatabasePool._pool:
            DatabasePool._pool.closeall()
            logging.info("Database connection pool closed.")