from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    rol_id: int = Field(..., description="Role ID of the user")
    name: str = Field(..., description="Name of the user")
    user: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

class UserResponse(UserCreate):
    id: int = Field(..., description="Unique identifier of the user")