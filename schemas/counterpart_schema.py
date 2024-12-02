from pydantic import BaseModel, Field

class CounterpartSchema(BaseModel):
    resourceid: int = Field(..., description="Unique identifier for the resource")
    resorucetype: str = Field(..., description="Type of the resource")
    entity: str = Field(..., description="Name of the entity")
    inkind: float = Field(..., description="In-kind value of the resource")
    cash: float = Field(..., description="Cash value of the resource")

class CounterpartResponse(CounterpartSchema):
    id: int = Field(..., description="Unique identifier for the counterpart")