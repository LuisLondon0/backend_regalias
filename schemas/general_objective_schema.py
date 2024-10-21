from pydantic import BaseModel, Field

class GeneralObjectiveCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255, description="Description of the general objective")

class GeneralObjectiveResponse(GeneralObjectiveCreate):
    id: int