from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import models
from internal.schemas import UserCreate, ServiceBase, RoleCreate, PermissionBase, RoleBase
from internal.security import get_password_hash


#region CREATE


def create_user(db: Session, user: UserCreate):
    '''
    Description:
    Creates a user in the database. Permissions must be added to this user separately by an admin.
    
    Parameters:
    - db: Database Session
    - user: User creation schema object
    '''
    hashed_pass = get_password_hash(user.password)
    db_user = models.User(username=user.username, full_name=user.full_name, email=user.email, hashed_password=hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_super_admin(db: Session, user: UserCreate):
    '''
    Description:
    Creates an user with administratives privileges. This function should only be used for initialization purposes.

    Parameters:
    - db: Database Session
    - user: User creation schema object with the role id set to 1 (admin)
    '''
    hashed_pass = get_password_hash(user.password)
    db_user = models.User(username=user.username, full_name=user.full_name, email=user.email, hashed_password=hashed_pass, role_id=2)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_service(db: Session, service: ServiceBase):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def create_role(db: Session, role: RoleCreate):
    if role.permissions:
        permissions_ids = []
        for permission in role.permissions:
            if isinstance(permission, int):
                db_permission = db.query(models.Permission).filter(models.Permission.id == permission).first()
            elif isinstance(permission, str):
                db_permission = db.query(models.Permission).filter(models.Permission.name == permission).first()
            else:
                raise Exception(f"Invalid permission type {type(permission)}")
            
            if not db_permission:
                raise Exception(f"Permission {permission} not found")

            permissions_ids.append(db_permission.id)

    try:
        db_role = models.Role(name=role.name)
        db.add(db_role)
        db.flush()

        role_permissions = [
            models.RolePermission(role_id=db_role.id, permission_id=permission_id)
            for permission_id in permissions_ids
        ]
        db.bulk_save_objects(role_permissions)

        db.commit()
        db.refresh(db_role)
        return db_role

    except IntegrityError as e:
        db.rollback()
        raise Exception("Role creation failed: " + str(e))

def create_permission(db: Session, permission: PermissionBase):
    db_permission = models.Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


#endregion CREATE

#region READ

#TODO: Add more endpoints for getting users by username, email, etc.
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_active_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()

def get_active_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email, models.User.is_active == True).first()

def get_active_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()


def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def get_services_by_name(db: Session, name: str):
    return db.query(models.Service).filter(models.Service.name == name).all()

def get_services_by_url(db: Session, url: str):
    return db.query(models.Service).filter(models.Service.url == url).all()

def get_active_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id, models.Service.is_active == True).first()

def get_active_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).filter(models.Service.is_active == True).offset(skip).limit(limit).all()

def get_active_services_by_name(db: Session, name: str):
    return db.query(models.Service).filter(models.Service.name == name, models.Service.is_active == True).all()

def get_active_services_by_url(db: Session, url: str):
    return db.query(models.Service).filter(models.Service.url == url, models.Service.is_active == True).all()


def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def get_role_permissions(db: Session, role_id: int):
    return db.query(models.Permission.name).join(models.RolePermission, models.Permission.id == models.RolePermission.permission_id).filter(models.RolePermission.role_id == role_id).all()


def get_permission_by_id(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

def get_permission_by_name(db: Session, name: str):
    #TODO: this should be a partial match because of the way permissions are stored: "service:endpoint"
    return db.query(models.Permission).filter(models.Permission.name == name).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()



#TODO: Also Implement these
def get_user_permissions(db: Session, user_id: int):
    pass

def get_service_permissions(db: Session, service_id: int):
    pass


#endregion READ

#region UPDATE


def update_user_role(db: Session, user_id: int, role_id: int):
    pass


#TODO: Also Implement these
def update_user(db: Session, user: UserCreate):
    raise NotImplementedError

def update_service(db: Session, service: ServiceBase):
    raise NotImplementedError

def update_role(db: Session, role: RoleBase):
    raise NotImplementedError

def update_permission(db: Session, permission: PermissionBase):
    raise NotImplementedError

def add_role_permission(db: Session, role_id: int, permission_id: int):
    raise NotImplementedError

def remove_user_role(db: Session, user_id: int, role_id: int):
    raise NotImplementedError

def remove_role_permission(db: Session, role_id: int, permission_id: int):
    raise NotImplementedError

def deactivate_user(db: Session, user_id: int):
    raise NotImplementedError

def deactivate_service(db: Session, service_id: int):
    raise NotImplementedError


#endregion UPDATE

#region DELETE


def delete_user(db: Session, user_id: int):
    raise NotImplementedError

def delete_service(db: Session, service_id: int):
    raise NotImplementedError

def delete_role(db: Session, role_id: int):
    raise NotImplementedError

def delete_permission(db: Session, permission_id: int):
    raise NotImplementedError


#endregion DELETE