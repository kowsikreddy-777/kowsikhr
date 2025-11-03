"""
Letter Template & History Repositories - Data Access Layer
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.letter import LetterTemplate, LetterHistory


class LetterTemplateRepository:
    """Repository for LetterTemplate model"""

    def get_all(self, db: Session) -> List[LetterTemplate]:
        """Get all letter templates"""
        return db.query(LetterTemplate).all()

    def get_by_id(self, db: Session, template_id: int) -> Optional[LetterTemplate]:
        """Get a letter template by ID"""
        return db.query(LetterTemplate).filter(LetterTemplate.id == template_id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[LetterTemplate]:
        """Get a letter template by name"""
        return db.query(LetterTemplate).filter(LetterTemplate.name == name).first()

    def get_offer_letters(self, db: Session) -> List[LetterTemplate]:
        """Get all offer letter templates"""
        return db.query(LetterTemplate).filter(LetterTemplate.is_offer_letter == True).all()

    def get_non_offer_letters(self, db: Session) -> List[LetterTemplate]:
        """Get all non-offer letter templates"""
        return db.query(LetterTemplate).filter(LetterTemplate.is_offer_letter == False).all()

    def create(self, db: Session, template_data: dict) -> LetterTemplate:
        """Create a new letter template"""
        template = LetterTemplate(**template_data)
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    def update(self, db: Session, template: LetterTemplate, update_data: dict) -> LetterTemplate:
        """Update an existing letter template"""
        for key, value in update_data.items():
            if value is not None:
                setattr(template, key, value)
        template.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(template)
        return template

    def delete(self, db: Session, template: LetterTemplate) -> bool:
        """Delete a letter template"""
        db.delete(template)
        db.commit()
        return True

    def exists_by_name(self, db: Session, name: str) -> bool:
        """Check if a letter template exists by name"""
        return db.query(LetterTemplate).filter(LetterTemplate.name == name).first() is not None

    def count_total(self, db: Session) -> int:
        """Count total letter templates"""
        return db.query(LetterTemplate).count()

    def count_offer_letters(self, db: Session) -> int:
        """Count offer letter templates"""
        return db.query(LetterTemplate).filter(LetterTemplate.is_offer_letter == True).count()


class LetterHistoryRepository:
    """Repository for LetterHistory model"""

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[LetterHistory]:
        """Get all letter history entries with pagination"""
        return db.query(LetterHistory).order_by(LetterHistory.requested_at.desc()).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, history_id: int) -> Optional[LetterHistory]:
        """Get a letter history entry by ID"""
        return db.query(LetterHistory).filter(LetterHistory.id == history_id).first()

    def get_by_letter_name(self, db: Session, letter_name: str) -> List[LetterHistory]:
        """Get letter history entries by letter name"""
        return db.query(LetterHistory).filter(LetterHistory.letter_name == letter_name)\
                 .order_by(LetterHistory.requested_at.desc()).all()

    def get_by_status(self, db: Session, status: str) -> List[LetterHistory]:
        """Get letter history entries by status"""
        return db.query(LetterHistory).filter(LetterHistory.status == status)\
                 .order_by(LetterHistory.requested_at.desc()).all()

    def get_recent(self, db: Session, limit: int = 10) -> List[LetterHistory]:
        """Get recent letter history entries"""
        return db.query(LetterHistory).order_by(LetterHistory.requested_at.desc()).limit(limit).all()

    def create(self, db: Session, history_data: dict) -> LetterHistory:
        """Create a new letter history entry"""
        history = LetterHistory(**history_data)
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def delete(self, db: Session, history: LetterHistory) -> bool:
        """Delete a letter history entry"""
        db.delete(history)
        db.commit()
        return True

    def count_total(self, db: Session) -> int:
        """Count total letter history entries"""
        return db.query(LetterHistory).count()

    def count_by_status(self, db: Session, status: str) -> int:
        """Count letter history entries by status"""
        return db.query(LetterHistory).filter(LetterHistory.status == status).count()
