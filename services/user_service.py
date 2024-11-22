from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserResponse
from services.role_service import RoleService
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import logging
import os
from fastapi import HTTPException

class UserService:
    def __init__(self):
        self.repo = UserRepository()
        self.role_service = RoleService()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.environ.get('R_SECRET_KEY')
        self.algorithm = os.environ.get('R_ALGORITHM')
        self.access_token_expire_minutes = int(os.environ.get('R_ACCESS_TOKEN_EXPIRE_MINUTES'))

    def create_user(self, user: UserCreate) -> UserResponse:
        existing_user = self.repo.get_user_by_username(user.user)
        if existing_user:
            raise ValueError("Username already exists")

        role = self.role_service.get_role_by_id(user.rol_id)
        if not role:
            raise ValueError("Role does not exist")

        if not user.name:
            raise ValueError("Name cannot be empty")

        if not user.user:
            raise ValueError("Username cannot be empty")

        if not user.password or len(user.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        user.name = user.name.strip()
        user.user = user.user.strip()
        user.password = self.hash_password(user.password.strip())

        response = self.repo.create_user(user)

        logging.info(f"User created with ID: {response.id}")

        return response

    def get_users(self):
        users = self.repo.get_users()
        return users

    def get_user_by_id(self, user_id: int):
        if user_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_user_by_id(user_id)

    def update_user(self, user_id: int, user: UserCreate) -> UserResponse:
        role = self.role_service.get_role_by_id(user.rol_id)
        if not role:
            raise ValueError("Role does not exist")

        if not user.name:
            raise ValueError("Name cannot be empty")

        if not user.user:
            raise ValueError("Username cannot be empty")

        if not user.password or len(user.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        user.name = user.name.strip()
        user.user = user.user.strip()
        user.password = self.hash_password(user.password.strip())

        response = self.repo.update_user(user_id, user)

        logging.info(f"User with ID: {user_id} updated")

        return response

    def delete_user(self, user_id: int) -> bool:
        if user_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_user(user_id)

        if success:
            logging.info(f"User with ID: {user_id} deleted")
        else:
            logging.warning(f"User with ID: {user_id} not found")

        return success

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str):
        user = self.repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.user, "id": user.id, "role": user.rol_id}, 
            expires_delta=access_token_expires
        )
        return access_token

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise JWTError("Invalid token")
            return {"username": username, "id": payload.get("id"), "role": payload.get("role")}
        except JWTError as e:
            logging.error(f"Token validation error: {e}")
            raise ValueError("Invalid or expired token")