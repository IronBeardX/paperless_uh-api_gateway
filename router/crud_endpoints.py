from fastapi import Depends, Query, Path, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from internal.schemas import UserCreate, User, RoleBase, Role, Service, ServiceBase, Permission, PermissionBase
from dependencies import get_db, get_current_active_user

from database import crud, models
from database.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(dependencies=[Depends(get_current_active_user)])


#region CREATE

@router.post("/create/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/create/services", response_model=Service)
def create_service(service: ServiceBase, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_url(db, name=service.url)
    if db_service:
        raise HTTPException(status_code=400, detail="Service already exists")
    return crud.create_service(db=db, service=service)


@router.post("/create/roles", response_model=Role)
def create_role(role: RoleBase, db: Session = Depends(get_db)):
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db=db, role=role)


@router.post("/create/permissions", response_model=Permission)
def create_permission(permission: PermissionBase, db: Session = Depends(get_db)):
    db_permission = crud.get_permission_by_name(db, name=permission.name)
    if db_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")
    return crud.create_permission(db=db, permission=permission)


@router.post("/create/role_permission", response_model=Role)
def create_role_permission(
    role_id: Annotated[int, Query()] =...,
    permission_id: Annotated[int, Query()] =...,
    db: Session = Depends(get_db)
    ):
    db_role = crud.get_role_by_id(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_permission = crud.get_permission_by_id(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    return crud.create_role_permission(db=db, role_id=role_id, permission_id=permission_id)


#endregion CREATE


#region READ


@router.get("/user", response_model=User)
def read_user(
    user_id: Annotated[int | None, Query()] = None, 
    user_email: Annotated[str | None, Query()] = None,
    active_only: Annotated[bool, Query()] = True,
    db: Session = Depends(get_db)
    ):
    if user_id:
        if active_only:
            db_user = crud.get_active_user_by_id(db, user_id=user_id)
        else:
            db_user = crud.get_user_by_id(db, user_id=user_id)
    elif user_email:
        if active_only:
            db_user = crud.get_active_user_by_email(db, email=user_email)
        else:
            db_user = crud.get_user_by_email(db, email=user_email)
    else:
        raise HTTPException(status_code=400, detail="User ID or Email must be provided")
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user


@router.get("/users", response_model=list[User])
def read_users(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
    active_only: Annotated[bool, Query()] = True,
    db: Session = Depends(get_db)
    ):
    if active_only:
        return crud.get_active_users(db, skip=skip, limit=limit)
    else:
        return crud.get_users(db, skip=skip, limit=limit)


@router.get("/service", response_model=Service)
def read_service(
    service_id: Annotated[int | None, Query()] = None,
    service_url: Annotated[str | None, Query()] = None,
    service_name: Annotated[str | None, Query()] = None,
    active_only: Annotated[bool, Query()] = True,
    db: Session = Depends(get_db)
    ):
    if service_id:
        if active_only:
            db_service = crud.get_active_service_by_id(db, service_id=service_id)
        else:
            db_service = crud.get_service_by_id(db, service_id=service_id)
    elif service_url:
        if active_only:
            db_service = crud.get_active_service_by_url(db, url=service_url)
        else:
            db_service = crud.get_service_by_url(db, url=service_url)
    elif service_name:
        if active_only:
            db_service = crud.get_active_service_by_name(db, name=service_name)
        else:
            db_service = crud.get_service_by_name(db, name=service_name)
    else:
        raise HTTPException(status_code=400, detail="Service ID, URL, or Name must be provided")
    
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return db_service


@router.get("/services", response_model=list[Service])
def read_services(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
    active_only: Annotated[bool, Query()] = True,
    db: Session = Depends(get_db)
    ):
    if active_only:
        return crud.get_active_services(db, skip=skip, limit=limit)
    else:
        return crud.get_services(db, skip=skip, limit=limit)


@router.get("/role", response_model=Role)
def read_role(
    role_id: Annotated[int | None, Query()] = None,
    role_name: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db)
    ):
    if role_id:
        db_role = crud.get_role_by_id(db, role_id=role_id)
    elif role_name:
        db_role = crud.get_role_by_name(db, name=role_name)
    else:
        raise HTTPException(status_code=400, detail="Role ID or Name must be provided")
    
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return db_role


@router.get("/roles", response_model=list[Role])
def read_roles(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
    db: Session = Depends(get_db)
    ):
    return crud.get_roles(db, skip=skip, limit=limit)


@router.get("/permission", response_model=Permission)
def read_permission(
    permission_id: Annotated[int | None, Query()] = None,
    permission_name: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db)
    ):
    if permission_id:
        db_permission = crud.get_permission_by_id(db, permission_id=permission_id)
    elif permission_name:
        db_permission = crud.get_permission_by_name(db, name=permission_name)
    else:
        raise HTTPException(status_code=400, detail="Permission ID or Name must be provided")
    
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    return db_permission


@router.get("/permissions", response_model=list[Permission])
def read_permissions(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
    db: Session = Depends(get_db)
    ):
    return crud.get_permissions(db, skip=skip, limit=limit)


#TODO: Implement These
@router.get("/user/{user_id}/permissions", response_model=list[Permission])
def read_user_services(
    user_id: int,
    db: Session = Depends(get_db)
    ):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/user/{service_id}/permissions", response_model=list[Permission])
def read_service_permissions(
    service_id: int,
    db: Session = Depends(get_db)
    ):
    raise HTTPException(status_code=501, detail="Not Implemented")


#endregion READ


#region UPDATE


@router.put("/user/{user_id}", response_model=User)
def update_user(
    user_id: Annotated[int, Path()],
    new_role_id: Annotated[int, Query()] = ...,
    db: Session = Depends(get_db)
    ):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_role = crud.get_role_by_id(db, role_id=new_role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_user.role_id = new_role_id
    db.commit()
    db.refresh(db_user)
    return db_user


#endregion UPDATE