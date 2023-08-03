from typing import Annotated
from fastapi import APIRouter, Depends, Path
from pydantic import HttpUrl

import httpx

from router.service_registry import discover_service #TODO: maybe make this in internal functions ?
from dependencies import get_current_active_user

router = APIRouter(dependencies=[Depends(get_current_active_user)])

#test_endpoint
@router.get("/testgateway")
async def test_endpoint():
    return {"message": "Hello World"}


@router.get("/{service_name}/{service_request:path}")
async def proxy_request(service_name: Annotated[str, Path()], service_request: Annotated[HttpUrl, Path()]):
    service_info = discover_service(service_name)
    if service_info.url:
        response = await httpx.get(f"{service_info.url}/{service_request}")
        return response.json()
    return {"message": f"{service_name} not found"}
