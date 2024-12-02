from database.database import DatabaseConnection
from schemas.user_schema import UserCreate, UserResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserRepository:
    def create_user(self, user: UserCreate) -> UserResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (roleid, name, username, password) VALUES (%s, %s, %s, %s) RETURNING userid", 
                        (user.rol_id, user.name, user.user, user.password)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return UserResponse(id=id, rol_id=user.rol_id, name=user.name, user=user.user, password=user.password)
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            raise

    def get_users(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users")
                    users = cursor.fetchall()
                    if users:
                        return [
                            UserResponse(id=user[0], rol_id=user[1], name=user[2], user=user[3], password=user[4]) 
                            for user in users
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching users: {e}")
            raise

    def get_user_by_id(self, user_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
                    user = cursor.fetchone()
                    if user:
                        return UserResponse(id=user[0], rol_id=user[1], name=user[2], user=user[3], password=user[4])
                    return None
        except Exception as e:
            logging.error(f"Error fetching user by id {user_id}: {e}")
            raise

    def get_user_by_username(self, username: str):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                    user = cursor.fetchone()
                    if user:
                        return UserResponse(id=user[0], rol_id=user[1], name=user[2], user=user[3], password=user[4])
                    return None
        except Exception as e:
            logging.error(f"Error fetching user by username {username}: {e}")

    def update_user(self, user_id: int, user: UserCreate) -> UserResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE users SET roleid = %s, name = %s, username = %s, password = %s WHERE userid = %s", 
                        (user.rol_id, user.name, user.user, user.password, user_id)
                    )
                    conn.commit()
                    return UserResponse(id=user_id, rol_id=user.rol_id, name=user.name, user=user.user, password=user.password)
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            raise

    def delete_user(self, user_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No user found with id {user_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            raise