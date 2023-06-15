from pydantic import BaseModel, HttpUrl


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

class ServiceInformation(BaseModel):
    url: HttpUrl