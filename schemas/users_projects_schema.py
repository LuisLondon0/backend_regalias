from pydantic import BaseModel, Field

class UserProjectCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user")
    project_id: int = Field(..., description="ID of the project")