@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    # Повертаємо контакти ТІЛЬКИ поточного користувача
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).all()
    return contacts

@router.post("/", response_model=ContactResponse, status_code=201)
async def create_contact(
    body: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    contact = Contact(**body.model_dump(), user_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact