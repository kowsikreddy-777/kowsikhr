"""
Pydantic Schemas for Notifications Management
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class SendOption(str, Enum):
    """Send option enumeration"""
    SEND_NOW = "send_now"
    SEND_LATER = "send_later"


class LocationOption(str, Enum):
    """Location options"""
    ALL_LOCATIONS = "all_locations"
    BANGALORE = "bangalore"
    HYDERABAD = "hyderabad"


class DepartmentOption(str, Enum):
    """Department options"""
    ALL_DEPARTMENTS = "all_departments"
    PRODUCT_DEVELOPMENT = "product_development"
    HR_EXECUTIVE = "hr_executive"
    TECHNICAL_SUPPORT = "technical_support"


class NotificationBase(BaseModel):
    """Base schema for Notification"""
    location: str = Field(..., description="Location: all_locations, bangalore, hyderabad")
    department: str = Field(..., description="Department: all_departments, product_development, hr_executive, technical_support")
    employee_search: Optional[str] = Field(None, description="Search term for specific employees")
    send_option: SendOption = Field(default=SendOption.SEND_NOW, description="Send now or schedule for later")
    subject: str = Field(..., min_length=1, max_length=255, description="Notification subject")
    description: str = Field(..., min_length=1, description="Notification description/message")
    scheduled_time: Optional[datetime] = Field(None, description="Scheduled time for send_later option")


class NotificationCreate(NotificationBase):
    """Schema for creating a new notification"""
    pass


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    location: Optional[str] = None
    department: Optional[str] = None
    employee_search: Optional[str] = None
    send_option: Optional[SendOption] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    scheduled_time: Optional[datetime] = None
    is_sent: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: int
    image_path: Optional[str] = None
    image_filename: Optional[str] = None
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for listing notifications"""
    id: int
    subject: str
    description: str
    location: str
    department: str
    is_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LocationList(BaseModel):
    """Available locations"""
    locations: list[dict] = [
        {"value": "all_locations", "label": "All Locations"},
        {"value": "bangalore", "label": "Bangalore"},
        {"value": "hyderabad", "label": "Hyderabad"}
    ]


class DepartmentList(BaseModel):
    """Available departments"""
    departments: list[dict] = [
        {"value": "all_departments", "label": "All Departments"},
        {"value": "product_development", "label": "Product Development Team"},
        {"value": "hr_executive", "label": "HR Executive"},
        {"value": "technical_support", "label": "Technical Support"}
    ]