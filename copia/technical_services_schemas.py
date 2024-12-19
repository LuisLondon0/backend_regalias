from pydantic import BaseModel, Field


class TechnicalServiceSchema(BaseModel):
    activity_id: int = Field(..., description="ID of the activity this technical service belongs to")
    entity: str = Field(..., description="Name of the entity or department providing the technical service")
    test_services: str = Field(..., description="Description of the technical services and tests to be performed")
    description: str = Field(..., description="Detailed description of the service scope and objectives")
    tech_specification: str = Field(..., description="Technical specifications and requirements of the service")
    quantity: int = Field(..., description="Number of service units required (must be positive)")
    unitvalue: float = Field(..., description="Cost per unit of service")
    cost: float = Field(..., description="Total cost of the service (must be non-negative)")


class TechnicalServiceResponse(TechnicalServiceSchema):
    id: int = Field(..., description="Unique identifier of the technical service record")
