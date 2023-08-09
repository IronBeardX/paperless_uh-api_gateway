#TODO: implement this file
from sqlalchemy.orm import Session

from database.crud import create_super_admin, create_role, create_permission
from database.database import SessionLocal
from internal.schemas import RoleCreate, UserCreate, PermissionBase

def initialize_database():
    #BUG: is this process was already done, it will raise an exception
    db = SessionLocal()
    try:
        # Create roles
        admin_role = RoleCreate(
            name="admin",
            permissions=[
                "*"
            ]
            )
        user_role = RoleCreate(
            name="new user",
            permissions=[
                "_"
            ]
            )

        # Create permissions
        admin_permission = PermissionBase(name="*")
        empty_permission = PermissionBase(name="_")

        # Create admin user
        admin_user = UserCreate(
            username="admin",
            full_name="admin",
            email="fakemail@fmail.com",
            password="admin"
        )

        # Add the records to the session
        create_permission(db, empty_permission)
        create_permission(db, admin_permission)

        create_role(db, user_role)
        create_role(db, admin_role)

        create_super_admin(db, admin_user)

    except Exception as e:
        db.rollback()
        #TODO: Make it so it tries to create the data one by one and log wich one was already created and wich one was'nt
    finally:
        db.close()