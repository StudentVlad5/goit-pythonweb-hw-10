from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Request

from database.db import get_db
from schemas.user import UserSchema, UserResponse, TokenSchema
from repository import users as repository_users
from services.auth import auth_service
from database.models import User
from services.limiter import limiter
from services.email import send_email
from config.config import settings

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, db: Session = Depends(get_db)):
    exist_user = repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    body.password = auth_service.get_password_hash(body.password)
    
    new_user = repository_users.create_user(body, db)
    
    host = settings.base_url
    await send_email(new_user.email, new_user.username, str(host))
    return new_user

@router.post("/login", response_model=TokenSchema)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=401, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
    
    repository_users.update_token(user, refresh_token, db)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me")
@limiter.limit("5/minute")
def me(
    request: Request,
    user: User = Depends(auth_service.get_current_user)
):
    return user

@router.get("/confirm_email/{token}")
def confirm_email(token: str, db: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = repository_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(status_code=400, detail="Verification error")
    if user.confirmed:
        return {"message": "Email already confirmed"}

    repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}