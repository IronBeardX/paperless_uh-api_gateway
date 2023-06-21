from typing import Annotated

from internal.schemas import User
from dependencies import get_current_active_user, get_db
from internal.security import authenticate_user, create_access_token

from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import yaml

#TODO: Delete this
# db = {
#     "admin": {
#         "username": "admin",
#         "full_name": "admin",
#         "email": "admin@super.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

router = APIRouter()

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
    ):
    #TODO: How to get the email in the form_data?
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    with open("config.yaml") as file:
        config = yaml.safe_load(file)
    access_token_expires_minutes = config["ACCESS_TOKEN_EXPIRE_MINUTES"]
    access_token_expires = timedelta(minutes = access_token_expires_minutes)
    access_token = create_access_token(data = {"sub": user.email}, expires_delta = access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
