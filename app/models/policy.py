"""
Database Models for Policy Management System
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base


class PolicyType(str, enum.Enum):
    """Policy type enumeration"""
    UPLOADED = "uploaded"
    ONLINE = "online"


class Policy(Base):
    """Policy model for storing company policies"""
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String(255), nullable=False, index=True)
    type = Column(Enum(PolicyType), nullable=False, default=PolicyType.UPLOADED)
    actions = Column(Boolean, nullable=True)

    # For uploaded policies
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    
    # For online policies
    content = Column(Text, nullable=True)
    
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    
    def __repr__(self):
        return f"<Policy(id={self.id}, name={self.policy_name}, type={self.type},actions={self.actions})>"