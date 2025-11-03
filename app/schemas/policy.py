"""
Pydantic Schemas for Policy Management
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class PolicyType(str, Enum):
    """Policy type enumeration"""
    UPLOADED = "uploaded"
    ONLINE = "online"


class PolicyBase(BaseModel):
    """Base schema for Policy"""
    policy_name: str = Field(..., min_length=1, max_length=255, description="Name of the policy")
    type: PolicyType = Field(..., description="Type of policy: uploaded or online")
    actions: Optional[bool] = Field(None, description="Whether actions are enabled for this policy")


class PolicyCreate(PolicyBase):
    """Schema for creating a new policy"""
    file_path: Optional[str] = Field(None, max_length=500, description="Path to uploaded policy file")
    file_name: Optional[str] = Field(None, max_length=255, description="Name of uploaded file")
    content: Optional[str] = Field(None, description="Content for online policy")


class PolicyUpdate(BaseModel):
    """Schema for updating a policy"""
    policy_name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[PolicyType] = None
    file_path: Optional[str] = Field(None, max_length=500)
    file_name: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    actions: Optional[bool] = None


class PolicyResponse(PolicyBase):
    """Schema for policy response"""
    id: int
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    content: Optional[str] = None
    created_on: datetime
    last_updated: datetime
    actions: Optional[bool] = None

    class Config:
        from_attributes = True


class PolicyListResponse(BaseModel):
    """Schema for listing policies"""
    id: int
    policy_name: str
    type: PolicyType
    created_on: datetime
    last_updated: datetime
    actions: Optional[bool] = None

    class Config:
        from_attributes = True