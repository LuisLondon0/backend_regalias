from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")

class LoginResponse(BaseModel):
    access_token: str = Field(..., description="The access token for authentication")
    token_type: str = Field(..., description="The type of the token, typically 'bearer'")