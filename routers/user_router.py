from fastapi import APIRouter, HTTPException, Depends
from typing import List
from services.user_service import UserService
from schemas.user_schema import UserCreate, UserResponse
from schemas.login_schema import LoginRequest, LoginResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
service = UserService()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return service.create_user(user)

@router.get("/users", response_model=List[UserResponse])
def get_users():
    return service.get_users()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    return service.update_user(user_id, user)

@router.delete("/users/{user_id}", response_model=bool)
def delete_user(user_id: int):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = service.authenticate_user(form_data.username, form_data.password)
    return LoginResponse(access_token=token, token_type="bearer")