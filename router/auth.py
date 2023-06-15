from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from models import User, UserInDB, TokenData, Token
# from dependencies import get_current_active_user, create_access_token, authenticate_user, oauth2_scheme

import yaml

#TODO: Delete this
db = {
    "admin": {
        "username": "admin",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

# # TODO: This should be taken from the config file
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
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

async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
    ):
    if current_user.disabled:
        raise HTTPException(status_code = 400, detail = "Inactive user")
    return current_user


router = APIRouter()


#test_endpoint
@router.get("/testauth")
async def test_endpoint():
    return {"message": "Hello World"}


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    with open("config.yaml", "r") as f:
        access_token_expires_conf = yaml.safe_load(f)["ACCESS_TOKEN_EXPIRE_MINUTES"]

    access_token_expires = timedelta(minutes=access_token_expires_conf)
    access_token = create_access_token(
        data = {"sub": user.username}, expires_delta = access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}#TODO: where goes the roles?




async def random_dep(token):
    return "maikel"

@router.get("/users/me", response_model=User)
async def test(
    current_user: Annotated[str, Depends(random_dep)]
    ):
    return current_user
# async def read_users_me(
#     current_user: Annotated[UserInDB, Depends(get_current_active_user)]
#     ):
#     return current_user

