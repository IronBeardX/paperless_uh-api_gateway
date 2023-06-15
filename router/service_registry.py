from typing import Annotated
from fastapi import APIRouter, Body, Path
from models import ServiceInformation


router = APIRouter()

#in memory database
services = {}#TODO: Use a database ?


#test_endpoint
@router.get("/testregister")
async def test_endpoint():
    return {"message": "Hello World"}


@router.get("/unregister/{service_name}")
async def unregister_service(service_name: Annotated[str, Path()]):
    if service_name not in services:
        return {"message": "Service not registered"}
    del services[service_name]
    return {"message": "Service unregistered"}


@router.get("/discover/{service_name}")
async def discover_service(service_name: Annotated[str, Path()]):
    service_info = services.get(service_name)
    if service_info:
        return {'service_name': service_name, 'service_url': service_info.url}
    return {"message": f"{service_name} not found in registry"}


@router.post("/register/{service_name}")
async def register_service(service_name: Annotated[str, Path()],
                            information: Annotated[ServiceInformation, Body()]):
    if service_name in services:
        return {"message": "Service already registered"}
    services[service_name] = ServiceInformation(url = information.url)
    return {"message": "Service registered"}

