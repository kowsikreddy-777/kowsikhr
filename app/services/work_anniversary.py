"""
Work Anniversary Service - Business Logic Layer for Work Anniversary Greetings
"""
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.repositories.work_anniversary_repository import WorkAnniversaryRepository
from app import models, schemas


class WorkAnniversaryService:
    """Service for Work Anniversary Greeting business logic"""
    
    def __init__(self):
        self.repository = WorkAnniversaryRepository()
    
    def get_all_greetings(self, db: Session) -> List[models.WorkAnniversaryGreeting]:
        """Get all work anniversary greetings"""
        return self.repository.get_all(db)
    
    def get_greeting_by_id(self, db: Session, greeting_id: int) -> models.WorkAnniversaryGreeting:
        """Get greeting by ID"""
        greeting = self.repository.get_by_id(db, greeting_id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Greeting not found")
        return greeting
    
    def create_greeting(
        self, 
        db: Session, 
        greeting_data: schemas.WorkAnniversaryGreetingCreate
    ) -> models.WorkAnniversaryGreeting:
        """Create a new work anniversary greeting"""
        return self.repository.create(db, greeting_data.dict())
    
    def update_greeting(
        self,
        db: Session,
        greeting_id: int,
        greeting_data: schemas.WorkAnniversaryGreetingCreate
    ) -> models.WorkAnniversaryGreeting:
        """Update an existing work anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        return self.repository.update(db, greeting, greeting_data.dict())
    
    def delete_greeting(self, db: Session, greeting_id: int) -> dict:
        """Delete a work anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        self.repository.delete(db, greeting)
        return {"message": f"Greeting {greeting_id} deleted successfully"}
    
    def get_enabled_greetings(self, db: Session) -> List[models.WorkAnniversaryGreeting]:
        """Get all enabled work anniversary greetings"""
        return self.repository.get_enabled_greetings(db)