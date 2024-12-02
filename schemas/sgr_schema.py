from pydantic import BaseModel, Field

class SGRSchema(BaseModel):
    resourceid: int = Field(..., description="Unique identifier for the resource")
    resourcetype: str = Field(..., min_length=1, max_length=255, description="Type of the resource")
    cash: float = Field(..., description="Cash value of the resource")

class SGRResponse(SGRSchema):
    id: int = Field(..., description="Unique identifier for the SGR")