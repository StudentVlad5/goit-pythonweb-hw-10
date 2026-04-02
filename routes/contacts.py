from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User
from schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from repository import contacts as repository_contacts
from services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get("/", response_model=List[ContactResponse])
def read_contacts(
    name: str = Query(None),
    last_name: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user) # ЗАХИСТ
):
    contacts = repository_contacts.get_contacts(name, last_name, email, current_user, db)
    return contacts

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    body: ContactCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    return repository_contacts.create_contact(body, current_user, db)

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    contact = repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int, 
    body: ContactUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    contact = repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    contact = repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return None