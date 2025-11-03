"""
Wedding Anniversary Repository - Data Access Layer for Wedding Anniversary Greetings
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models


class WeddingAnniversaryRepository:
    """Repository for WeddingAnniversaryGreeting model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.WeddingAnniversaryGreeting]:
        """Get all wedding anniversary greetings with pagination"""
        return db.query(models.WeddingAnniversaryGreeting).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, greeting_id: int) -> Optional[models.WeddingAnniversaryGreeting]:
        """Get wedding anniversary greeting by ID"""
        return db.query(models.WeddingAnniversaryGreeting).filter(
            models.WeddingAnniversaryGreeting.id == greeting_id
        ).first()
    
    def create(self, db: Session, greeting_data: dict) -> models.WeddingAnniversaryGreeting:
        """Create a new wedding anniversary greeting"""
        db_greeting = models.WeddingAnniversaryGreeting(**greeting_data)
        db.add(db_greeting)
        db.commit()
        db.refresh(db_greeting)
        return db_greeting
    
    def update(self, db: Session, greeting: models.WeddingAnniversaryGreeting, update_data: dict) -> models.WeddingAnniversaryGreeting:
        """Update an existing wedding anniversary greeting"""
        for key, value in update_data.items():
            if value is not None:
                setattr(greeting, key, value)
        db.commit()
        db.refresh(greeting)
        return greeting
    
    def delete(self, db: Session, greeting: models.WeddingAnniversaryGreeting) -> bool:
        """Delete a wedding anniversary greeting"""
        db.delete(greeting)
        db.commit()
        return True
    
    def get_enabled_greetings(self, db: Session) -> List[models.WeddingAnniversaryGreeting]:
        """Get all enabled wedding anniversary greetings"""
        return db.query(models.WeddingAnniversaryGreeting).filter(
            models.WeddingAnniversaryGreeting.enable == True
        ).all()