#TODO: implement this file
from sqlalchemy.orm import Session

from database.crud import create_super_admin, create_role, create_permission
from internal.schemas import RoleBase, UserCreate, Permission

def initialize_database(db: Session):
    try:
        # Create roles
        admin_role = RoleBase(name="admin")
        user_role = RoleBase(name="new user")

        # Create permissions
        admin_permission = Permission(permission_name="*")
        empty_permission = Permission(permission_name="_")

        # Create admin user
        admin_user = UserCreate(
            username="admin",
            full_name="admin",
            email="fakemail@fmail.com",
            password="admin"
        )

        # Add the records to the session
        create_role(db, user_role)
        create_role(db, admin_role)

        create_permission(db, empty_permission)
        create_permission(db, admin_permission)

        create_super_admin(db, admin_user)

    except Exception as e:
        print(e)
        raise e
    finally:
        db.close()