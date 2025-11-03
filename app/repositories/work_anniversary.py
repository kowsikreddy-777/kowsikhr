"""
Work Anniversary Repository - Data Access Layer for Work Anniversary Greetings
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models


class WorkAnniversaryRepository:
    """Repository for WorkAnniversaryGreeting model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.WorkAnniversaryGreeting]:
        """Get all work anniversary greetings with pagination"""
        return db.query(models.WorkAnniversaryGreeting).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, greeting_id: int) -> Optional[models.WorkAnniversaryGreeting]:
        """Get work anniversary greeting by ID"""
        return db.query(models.WorkAnniversaryGreeting).filter(
            models.WorkAnniversaryGreeting.id == greeting_id
        ).first()
    
    def create(self, db: Session, greeting_data: dict) -> models.WorkAnniversaryGreeting:
        """Create a new work anniversary greeting"""
        db_greeting = models.WorkAnniversaryGreeting(**greeting_data)
        db.add(db_greeting)
        db.commit()
        db.refresh(db_greeting)
        return db_greeting
    
    def update(self, db: Session, greeting: models.WorkAnniversaryGreeting, update_data: dict) -> models.WorkAnniversaryGreeting:
        """Update an existing work anniversary greeting"""
        for key, value in update_data.items():
            if value is not None:
                setattr(greeting, key, value)
        db.commit()
        db.refresh(greeting)
        return greeting
    
    def delete(self, db: Session, greeting: models.WorkAnniversaryGreeting) -> bool:
        """Delete a work anniversary greeting"""
        db.delete(greeting)
        db.commit()
        return True
    
    def get_enabled_greetings(self, db: Session) -> List[models.WorkAnniversaryGreeting]:
        """Get all enabled work anniversary greetings"""
        return db.query(models.WorkAnniversaryGreeting).filter(
            models.WorkAnniversaryGreeting.enable == True
        ).all()