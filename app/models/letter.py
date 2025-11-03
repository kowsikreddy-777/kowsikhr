from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base


class LetterTemplate(Base):
    __tablename__ = "letter_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    file_path = Column(String, nullable=False)
    is_offer_letter = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)


class LetterHistory(Base):
    __tablename__ = "letter_history"

    id = Column(Integer, primary_key=True, index=True)
    letter_name = Column(String, nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Completed")