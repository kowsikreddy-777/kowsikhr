"""
Birthday Greeting Repository - Data Access Layer for Birthday Greetings
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models


class BirthdayGreetingRepository:
    """Repository for BirthdayGreeting model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.BirthdayGreeting]:
        """Get all birthday greetings with pagination"""
        return db.query(models.BirthdayGreeting).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, greeting_id: int) -> Optional[models.BirthdayGreeting]:
        """Get birthday greeting by ID"""
        return db.query(models.BirthdayGreeting).filter(models.BirthdayGreeting.id == greeting_id).first()
    
    def create(self, db: Session, greeting_data: dict) -> models.BirthdayGreeting:
        """Create a new birthday greeting"""
        db_greeting = models.BirthdayGreeting(**greeting_data)
        db.add(db_greeting)
        db.commit()
        db.refresh(db_greeting)
        return db_greeting
    
    def update(self, db: Session, greeting: models.BirthdayGreeting, update_data: dict) -> models.BirthdayGreeting:
        """Update an existing birthday greeting"""
        for key, value in update_data.items():
            if value is not None:
                setattr(greeting, key, value)
        db.commit()
        db.refresh(greeting)
        return greeting
    
    def delete(self, db: Session, greeting: models.BirthdayGreeting) -> bool:
        """Delete a birthday greeting"""
        db.delete(greeting)
        db.commit()
        return True
    
    def get_enabled_greetings(self, db: Session) -> List[models.BirthdayGreeting]:
        """Get all enabled birthday greetings"""
        return db.query(models.BirthdayGreeting).filter(
            models.BirthdayGreeting.enable == True
        ).all()