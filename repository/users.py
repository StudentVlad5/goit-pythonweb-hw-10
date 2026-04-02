from sqlalchemy.orm import Session
from database.models import User
from schemas.user import UserSchema

def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(body: UserSchema, db: Session) -> User:
    new_user = User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()

def confirmed_email(email: str, db: Session) -> None:
    user = get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

def update_avatar(email: str, url: str, db: Session) -> User:
    user = get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user