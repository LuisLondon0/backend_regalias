from database.database_pool import DatabasePool

class DatabaseConnection:
    def __enter__(self):
        self.conn = DatabasePool.get_connection()
        if self.conn is None:
            raise ConnectionError("Failed to establish database connection.")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            DatabasePool.release_connection(self.conn)