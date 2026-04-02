from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import settings
from database.models import Base

engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функція для створення всіх таблиць у БД
def init_db():
    Base.metadata.create_all(bind=engine)