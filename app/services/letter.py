"""
Letter Service - Business Logic Layer for Letters
"""

from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.repositories.letter_repository import LetterTemplateRepository, LetterHistoryRepository
from app import models, schemas


class LetterTemplateService:
    """Service for LetterTemplate business logic"""

    def __init__(self):
        self.repository = LetterTemplateRepository()

    def get_all_templates(self, db: Session) -> List[models.LetterTemplate]:
        """Get all letter templates"""
        return self.repository.get_all(db)

    def get_template_by_id(self, db: Session, template_id: int) -> models.LetterTemplate:
        """Get letter template by ID"""
        template = self.repository.get_by_id(db, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Letter template not found")
        return template

    def get_template_by_name(self, db: Session, name: str) -> models.LetterTemplate:
        """Get letter template by name"""
        template = self.repository.get_by_name(db, name)
        if not template:
            raise HTTPException(status_code=404, detail="Letter template not found")
        return template

    def create_template(self, db: Session, template_data: schemas.LetterTemplateCreate) -> models.LetterTemplate:
        """Create a new letter template"""
        return self.repository.create(db, template_data.dict())

    def update_template(self, db: Session, template_id: int, template_data: schemas.LetterTemplateUpdate) -> models.LetterTemplate:
        """Update an existing letter template"""
        template = self.get_template_by_id(db, template_id)
        return self.repository.update(db, template, template_data.dict())

    def delete_template(self, db: Session, template_id: int) -> dict:
        """Delete a letter template"""
        template = self.get_template_by_id(db, template_id)
        self.repository.delete(db, template)
        return {"message": "Letter template deleted successfully"}

    def get_offer_templates(self, db: Session) -> List[models.LetterTemplate]:
        """Get all offer letter templates"""
        return self.repository.get_offer_letters(db)

    def get_non_offer_templates(self, db: Session) -> List[models.LetterTemplate]:
        """Get all non-offer letter templates"""
        return self.repository.get_non_offer_letters(db)


class LetterHistoryService:
    """Service for LetterHistory business logic"""

    def __init__(self):
        self.repository = LetterHistoryRepository()

    def get_all_histories(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.LetterHistory]:
        """Get all letter history entries with pagination"""
        return self.repository.get_all(db, skip=skip, limit=limit)

    def get_history_by_id(self, db: Session, history_id: int) -> models.LetterHistory:
        """Get letter history by ID"""
        history = self.repository.get_by_id(db, history_id)
        if not history:
            raise HTTPException(status_code=404, detail="Letter history not found")
        return history

    def get_histories_by_letter_name(self, db: Session, letter_name: str) -> List[models.LetterHistory]:
        """Get letter history entries by letter name"""
        return self.repository.get_by_letter_name(db, letter_name)

    def get_histories_by_status(self, db: Session, status: str) -> List[models.LetterHistory]:
        """Get letter history entries by status"""
        return self.repository.get_by_status(db, status)

    def get_recent_histories(self, db: Session, limit: int = 10) -> List[models.LetterHistory]:
        """Get recent letter history entries"""
        return self.repository.get_recent(db, limit=limit)

    def create_history(self, db: Session, history_data: schemas.LetterHistoryCreate) -> models.LetterHistory:
        """Create a new letter history entry"""
        return self.repository.create(db, history_data.dict())

    def delete_history(self, db: Session, history_id: int) -> dict:
        """Delete a letter history entry"""
        history = self.get_history_by_id(db, history_id)
        self.repository.delete(db, history)
        return {"message": "Letter history deleted successfully"}
