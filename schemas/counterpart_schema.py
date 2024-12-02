from pydantic import BaseModel, Field

class CounterpartSchema(BaseModel):
    resourceid: int = Field(..., description="Unique identifier for the resource")
    resorucetype: str = Field(..., min_length=1, max_length=255, description="Type of the resource")
    entity: str = Field(..., min_length=1, max_length=255, description="Name of the entity")
    inkind: float = Field(..., description="In-kind value of the resource")
    cash: float = Field(..., description="Cash value of the resource")

class CounterpartResponse(CounterpartSchema):
    id: int = Field(..., description="Unique identifier for the counterpart")