from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

router = APIRouter()

#test_endpoint
@router.get("/testauth")
async def test_endpoint():
    return {"message": "Hello World"}
