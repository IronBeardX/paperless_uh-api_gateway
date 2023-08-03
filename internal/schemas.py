from pydantic import BaseModel, HttpUrl

class UserBase(BaseModel):
    username: str
    full_name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    role_id: int  = 0

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    name: str
    description: str
    url: HttpUrl
    endpoints: dict

class Service(ServiceBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    name: str

class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    permissions: list[ int|str ]

class Role(RoleBase):
    id: int
    permissions: list[ str ]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
    role: str = None

