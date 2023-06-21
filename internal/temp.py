from sqlalchemy.orm import Session

from database import models
from internal.schemas import UserCreate, ServiceBase, RoleBase, PermissionBase

def get_active_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email, models.User.is_active == True).first()
