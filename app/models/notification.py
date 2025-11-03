"""
Database Models for Notifications System
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class SendOption(str, enum.Enum):
    """Send option enumeration"""
    SEND_NOW = "send_now"
    SEND_LATER = "send_later"


class Notification(Base):
    """Notification model for employee notifications"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # Recipient Selection
    location = Column(String(100), nullable=False, index=True)  
    department = Column(String(100), nullable=False, index=True)  
    employee_search = Column(String(255), nullable=True)  
    
    # Message Details
    send_option = Column(SQLEnum(SendOption), nullable=False, default=SendOption.SEND_NOW)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Image attachment (optional)
    image_path = Column(String(500), nullable=True)
    image_filename = Column(String(255), nullable=True)
    
    # Send scheduling
    scheduled_time = Column(DateTime(timezone=True), nullable=True)  # For "send later"
    
    # Status tracking
    is_sent = Column(Boolean, default=False, nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, subject={self.subject}, location={self.location}, department={self.department})>"