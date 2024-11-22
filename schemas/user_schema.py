from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    rol_id: int = Field(..., description="Role ID of the user")
    name: str = Field(..., min_length=1, max_length=255, description="Name of the user")
    user: str = Field(..., min_length=1, max_length=255, description="Username of the user")
    password: str = Field(..., min_length=1, max_length=255, description="Password of the user")

class UserResponse(UserCreate):
    id: int = Field(..., description="Unique identifier of the user")