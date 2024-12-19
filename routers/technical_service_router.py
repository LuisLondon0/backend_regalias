from fastapi import APIRouter, HTTPException
from services.technical_service_service import TechnicalServiceService
from schemas.technical_services_schemas import (
    TechnicalServiceSchema,
    TechnicalServiceResponse,
)

router = APIRouter()
service = TechnicalServiceService()


@router.get(
    "/technical_service",
    response_model=list[TechnicalServiceResponse],
)
def get_technical_services():
    return service.get_technical_services()


@router.post(
    "/technical_service",
    response_model=TechnicalServiceResponse,
)
def create_technical_service(technical_service: TechnicalServiceSchema):
    return service.create_technical_service(technical_service)


@router.get(
    "/technical_service/{technical_service_id}",
    response_model=TechnicalServiceResponse,
)
def get_technical_service_by_id(technical_service_id: int):
    technical_service = service.get_technical_service_by_id(technical_service_id)
    if technical_service is None:
        raise HTTPException(status_code=404, detail="Technical service not found")
    return technical_service


@router.put(
    "/technical_service/{technical_service_id}",
    response_model=TechnicalServiceResponse,
)
def update_technical_service(
    technical_service_id: int, technical_service: TechnicalServiceSchema
):
    return service.update_technical_service(
        technical_service_id,
        technical_service,
    )


@router.delete(
    "/technical_service/{technical_service_id}",
    response_model=bool,
)
def delete_technical_service(technical_service_id: int):
    success = service.delete_technical_service(technical_service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Technical service not found")
    return success
