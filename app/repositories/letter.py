from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.letter import LetterTemplate, LetterHistory


class LetterTemplateRepository:
    """Repository for Letter Template data access operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, template_data: dict) -> LetterTemplate:
        """Create a new letter template"""
        template = LetterTemplate(**template_data)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def get_by_id(self, template_id: int) -> Optional[LetterTemplate]:
        """Get letter template by ID"""
        return self.db.query(LetterTemplate).filter(
            LetterTemplate.id == template_id
        ).first()
    
    def get_by_name(self, name: str) -> Optional[LetterTemplate]:
        """Get letter template by name"""
        return self.db.query(LetterTemplate).filter(
            LetterTemplate.name == name
        ).first()
    
    def get_all(self) -> List[LetterTemplate]:
        """Get all letter templates"""
        return self.db.query(LetterTemplate).all()
    
    def get_offer_letters(self) -> List[LetterTemplate]:
        """Get all offer letter templates"""
        return self.db.query(LetterTemplate).filter(
            LetterTemplate.is_offer_letter == True
        ).all()
    
    def get_non_offer_letters(self) -> List[LetterTemplate]:
        """Get all non-offer letter templates"""
        return self.db.query(LetterTemplate).filter(
            LetterTemplate.is_offer_letter == False
        ).all()
    
    def update(self, template_id: int, template_data: dict) -> Optional[LetterTemplate]:
        """Update letter template by ID"""
        template = self.get_by_id(template_id)
        if not template:
            return None
        
        for key, value in template_data.items():
            if value is not None:
                setattr(template, key, value)
        
        template.last_updated = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def delete(self, template_id: int) -> bool:
        """Delete letter template by ID"""
        template = self.get_by_id(template_id)
        if not template:
            return False
        
        self.db.delete(template)
        self.db.commit()
        return True
    
    def exists_by_name(self, name: str) -> bool:
        """Check if letter template exists by name"""
        return self.db.query(LetterTemplate).filter(
            LetterTemplate.name == name
        ).first() is not None
    
    def count_total(self) -> int:
        """Count total letter templates"""
        return self.db.query(LetterTemplate).count()
    
    def count_offer_letters(self) -> int:
        """Count offer letter templates"""
        return self.db.query(LetterTemplate).filter(
            LetterTemplate.is_offer_letter == True
        ).count()


class LetterHistoryRepository:
    """Repository for Letter History data access operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, history_data: dict) -> LetterHistory:
        """Create a new letter history entry"""
        history = LetterHistory(**history_data)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history
    
    def get_by_id(self, history_id: int) -> Optional[LetterHistory]:
        """Get letter history by ID"""
        return self.db.query(LetterHistory).filter(
            LetterHistory.id == history_id
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[LetterHistory]:
        """Get all letter history with pagination"""
        return self.db.query(LetterHistory).order_by(
            LetterHistory.requested_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_letter_name(self, letter_name: str) -> List[LetterHistory]:
        """Get letter history by letter name"""
        return self.db.query(LetterHistory).filter(
            LetterHistory.letter_name == letter_name
        ).order_by(LetterHistory.requested_at.desc()).all()
    
    def get_by_status(self, status: str) -> List[LetterHistory]:
        """Get letter history by status"""
        return self.db.query(LetterHistory).filter(
            LetterHistory.status == status
        ).order_by(LetterHistory.requested_at.desc()).all()
    
    def get_recent(self, limit: int = 10) -> List[LetterHistory]:
        """Get recent letter history"""
        return self.db.query(LetterHistory).order_by(
            LetterHistory.requested_at.desc()
        ).limit(limit).all()
    
    def delete(self, history_id: int) -> bool:
        """Delete letter history by ID"""
        history = self.get_by_id(history_id)
        if not history:
            return False
        
        self.db.delete(history)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        """Count total letter history entries"""
        return self.db.query(LetterHistory).count()
    
    def count_by_status(self, status: str) -> int:
        """Count letter history by status"""
        return self.db.query(LetterHistory).filter(
            LetterHistory.status == status
        ).count()