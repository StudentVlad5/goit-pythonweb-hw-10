import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import  _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


from routes import auth, contacts, users
from database.db import engine
from database.models import Base
from services.limiter import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts REST API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 1. Налаштування CORS
# Дозволяємо доступ з будь-яких джерел (можна обмежити конкретними доменами)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Підключаємо маршрути (Router)
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Welcome to Contacts API. Go to /docs for Swagger UI"}

# Приклад маршруту з обмеженням швидкості (Rate Limiting)
@app.get("/api/healthchecker")
@limiter.limit("5/minute")
async def healthchecker(request: Request):
    return {"status": "OK", "message": "Welcome to FastAPI!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)