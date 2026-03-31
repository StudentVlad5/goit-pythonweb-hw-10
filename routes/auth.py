from services.email import create_email_token

@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(body: UserSchema, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=409, detail="Account already exists")

    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    token = create_email_token({"sub": new_user.email})

    print(f"Verify link: http://localhost:8000/api/auth/confirm/{token}")

    return new_user


@router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None or not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.confirmed:
        raise HTTPException(status_code=401, detail="Email not confirmed")
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/confirm/{token}")
async def confirm_email(token: str, db: Session = Depends(get_db)):
    email = jwt.decode(token, auth_service.SECRET_KEY, algorithms=["HS256"])["sub"]
    user = await repository_users.get_user_by_email(email, db)

    user.confirmed = True
    db.commit()

    return {"message": "Email confirmed"}