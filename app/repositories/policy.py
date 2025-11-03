"""
Policy Repository - Data Access Layer for Policies
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from app import models


class PolicyRepository:
    """Repository for Policy model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Policy]:
        """Get all policies with pagination"""
        return db.query(models.Policy).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, policy_id: int) -> Optional[models.Policy]:
        """Get policy by ID"""
        return db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    
    def create(self, db: Session, policy_data: dict) -> models.Policy:
        """Create a new policy"""
        db_policy = models.Policy(**policy_data)
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        return db_policy
    
    def update(self, db: Session, policy: models.Policy, update_data: dict) -> models.Policy:
        """Update an existing policy"""
        for key, value in update_data.items():
            if value is not None:
                setattr(policy, key, value)
        db.commit()
        db.refresh(policy)
        return policy
    
    def delete(self, db: Session, policy: models.Policy) -> bool:
        """Delete a policy"""
        db.delete(policy)
        db.commit()
        return True
    
    def get_by_type(self, db: Session, policy_type: models.PolicyType) -> List[models.Policy]:
        """Get policies by type"""
        return db.query(models.Policy).filter(models.Policy.type == policy_type).all()
    
    def get_uploaded_policies(self, db: Session) -> List[models.Policy]:
        """Get all uploaded policies"""
        return self.get_by_type(db, models.PolicyType.UPLOADED)
    
    def get_online_policies(self, db: Session) -> List[models.Policy]:
        """Get all online policies"""
        return self.get_by_type(db, models.PolicyType.ONLINE)
    
    def delete_with_file(self, db: Session, policy: models.Policy) -> bool:
        """Delete policy and associated file"""
        # Delete associated file if exists
        if policy.file_path and os.path.exists(policy.file_path):
            try:
                os.remove(policy.file_path)
            except Exception:
                pass
        
        db.delete(policy)
        db.commit()
        return True
    
    def get_by_name(self, db: Session, policy_name: str) -> Optional[models.Policy]:
        """Get policy by name"""
        return db.query(models.Policy).filter(models.Policy.policy_name == policy_name).first()