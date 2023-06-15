from typing import Annotated
from jose import JWTError, jwt

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from models import User, TokenData
from internal.security import get_user

import yaml

#TODO: Delete this when database is implemented
db = {
    "admin": {
        "username": "admin",
        "full_name": "admin",
        "email": "admin@super.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/token")# does this goes here?


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        with open("config.yaml") as file:
            config = yaml.safe_load(file)
        secret_key = config["SECRET_KEY"]
        algorithm = config["ALGORITHM"]

        payload = jwt.decode(token, secret_key, algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username = token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code = 400, detail = "Inactive user")
        return current_user