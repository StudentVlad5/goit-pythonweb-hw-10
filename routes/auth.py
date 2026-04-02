from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.db import get_db
from schemas.user import UserSchema, UserResponse, TokenSchema
from repository import users as repository_users
from services.auth import auth_service

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body: UserSchema, db: Session = Depends(get_db)):
    # 1. Перевіряємо, чи користувач вже існує
    exist_user = repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    # 2. Хешуємо пароль перед збереженням
    body.password = auth_service.get_password_hash(body.password)
    
    # 3. Створюємо користувача в БД
    new_user = repository_users.create_user(body, db)
    return new_user

@router.post("/login", response_model=TokenSchema)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Шукаємо користувача за email (у OAuth2 username — це зазвичай email)
    user = repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    
    # 2. Перевіряємо пароль
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    # 3. Генеруємо токени
    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
    
    # 4. Зберігаємо refresh_token у базі для безпеки
    repository_users.update_token(user, refresh_token, db)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}