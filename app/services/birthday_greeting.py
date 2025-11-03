"""
Birthday Greeting Service - Business Logic Layer for Birthday Greetings
"""
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.repositories.birthday_repository import BirthdayGreetingRepository
from app import models, schemas


class BirthdayGreetingService:
    """Service for Birthday Greeting business logic"""
    
    def __init__(self):
        self.repository = BirthdayGreetingRepository()
    
    def get_all_greetings(self, db: Session) -> List[models.BirthdayGreeting]:
        """Get all birthday greetings"""
        return self.repository.get_all(db)
    
    def get_greeting_by_id(self, db: Session, greeting_id: int) -> models.BirthdayGreeting:
        """Get greeting by ID"""
        greeting = self.repository.get_by_id(db, greeting_id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Birthday greeting not found")
        return greeting
    
    def create_greeting(self, db: Session, greeting_data: schemas.BirthdayGreetingBase) -> models.BirthdayGreeting:
        """Create a new birthday greeting"""
        return self.repository.create(db, greeting_data.dict())
    
    def update_greeting(self, db: Session, greeting_id: int, greeting_data: schemas.BirthdayGreetingBase) -> models.BirthdayGreeting:
        """Update an existing birthday greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        return self.repository.update(db, greeting, greeting_data.dict())
    
    def delete_greeting(self, db: Session, greeting_id: int) -> dict:
        """Delete a birthday greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        self.repository.delete(db, greeting)
        return {"message": f"Birthday greeting {greeting_id} deleted successfully"}
    
    def get_enabled_greetings(self, db: Session) -> List[models.BirthdayGreeting]:
        """Get all enabled birthday greetings"""
        return self.repository.get_enabled_greetings(db)