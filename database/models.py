from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from database.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    username = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('roles.id'), default=None)

    role = relationship('Role', back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)

    users = relationship('User', back_populates='role')

class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(String(255), unique=True, index=True)

class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.permission_id'), primary_key=True)

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    url = Column(String(255), unique=True)
    # endpoints = Column(JSONB) #test with this if we are using the postgree database
    endpoints = Column(Text) #test with this if we are using the sqlite database