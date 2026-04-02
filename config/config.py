from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str = "HS256"
    
    # Cloudinary 
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    
    # Пошта
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str

    # Використовуємо property, щоб Pydantic не шукав це поле в .env
    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = ConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()