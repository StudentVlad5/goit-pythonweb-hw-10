from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User
from schemas.user import UserResponse
from services.auth import auth_service
from services.cloudinary import cloudinary_service
from repository import users as repository_users

router = APIRouter(prefix="/users", tags=["users"])

@router.patch('/avatar', response_model=UserResponse)
def update_avatar_user(
    file: UploadFile = File(), 
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    public_id = f"ContactsApp/{current_user.username}"
    url = cloudinary_service.upload_image(file.file, public_id)
    user = repository_users.update_avatar(current_user.email, url, db)
    return user