"""
Wedding Anniversary Service - Business Logic Layer for Wedding Anniversary Greetings
"""
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.repositories.wedding_anniversary_repository import WeddingAnniversaryRepository
from app import models, schemas


class WeddingAnniversaryService:
    """Service for Wedding Anniversary Greeting business logic"""
    
    def __init__(self):
        self.repository = WeddingAnniversaryRepository()
    
    def get_all_greetings(self, db: Session) -> List[models.WeddingAnniversaryGreeting]:
        """Get all wedding anniversary greetings"""
        return self.repository.get_all(db)
    
    def get_greeting_by_id(self, db: Session, greeting_id: int) -> models.WeddingAnniversaryGreeting:
        """Get greeting by ID"""
        greeting = self.repository.get_by_id(db, greeting_id)
        if not greeting:
            raise HTTPException(
                status_code=404, 
                detail="Wedding anniversary greeting not found"
            )
        return greeting
    
    def create_greeting(
        self, 
        db: Session, 
        greeting_data: schemas.WeddingAnniversaryGreetingBase
    ) -> models.WeddingAnniversaryGreeting:
        """Create a new wedding anniversary greeting"""
        return self.repository.create(db, greeting_data.dict())
    
    def update_greeting(
        self,
        db: Session,
        greeting_id: int,
        greeting_data: schemas.WeddingAnniversaryGreetingBase
    ) -> models.WeddingAnniversaryGreeting:
        """Update an existing wedding anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        return self.repository.update(db, greeting, greeting_data.dict())
    
    def delete_greeting(self, db: Session, greeting_id: int) -> dict:
        """Delete a wedding anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        self.repository.delete(db, greeting)
        return {"message": f"Wedding anniversary greeting {greeting_id} deleted successfully"}
    
    def get_enabled_greetings(self, db: Session) -> List[models.WeddingAnniversaryGreeting]:
        """Get all enabled wedding anniversary greetings"""
        return self.repository.get_enabled_greetings(db)