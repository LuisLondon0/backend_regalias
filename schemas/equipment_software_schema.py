from pydantic import BaseModel, Field

class EquipmentSoftwareSchema(BaseModel):
    activity_id: int = Field(..., description="Unique identifier for the activity")
    entity: str = Field(..., description="Name of the entity")
    description: str = Field(..., description="Description of the software")
    justification: str = Field(..., description="Justification for the software")
    quantity: int = Field(..., description="Quantity of software")
    propertyoradministration: str = Field(..., description="Property or administration")
    unitvalue: float = Field(..., description="Unit value of the software")
    total: float = Field(..., description="Total value of the software")

class EquipmentSoftwareResponse(EquipmentSoftwareSchema):
    id: int = Field(..., description="Unique identifier for the software")