from internal.schemas import User, UserBase
from internal.temp import get_active_user_by_email

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

import yaml

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_user(db, email: str):
    user_dict = get_active_user_by_email(db, email)
    if user_dict:
        return UserBase(**user_dict)
    
def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    to_encode.update({"exp": expire})

    with open("config.yaml") as file:
        config = yaml.safe_load(file)
    secret_key = config['SECRET_KEY']
    algorithm = config['ALGORITHM']

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password): 
    return pwd_context.hash(password)