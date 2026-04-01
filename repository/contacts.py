from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database.models import Contact, User
from schemas.contact import ContactCreate, ContactUpdate

async def get_contacts(name: str, last_name: str, email: str, user: User, db: Session) -> List[Contact]:
    query = db.query(Contact).filter(Contact.user_id == user.id)
    if name:
        query = query.filter(Contact.first_name.ilike(f"%{name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

async def create_contact(body: ContactCreate, user: User, db: Session) -> Contact:
    contact = Contact(**body.model_dump(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = await get_contact(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = await get_contact(contact_id, user, db)
    if contact:
        for key, value in body.model_dump().items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
    return contact