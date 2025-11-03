"""
Policy Service - Business Logic Layer for Policies
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from pathlib import Path
import os
import shutil
from fastapi import HTTPException, UploadFile

from app.repositories.policy_repository import PolicyRepository
from app import models


class PolicyService:
    """Service for Policy business logic"""
    
    def __init__(self):
        self.repository = PolicyRepository()
        self.upload_dir = Path("uploads/policies")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_policy_type(self, type_str: str) -> models.PolicyType:
        """Validate and convert policy type"""
        try:
            return models.PolicyType(type_str)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid policy type. Use 'uploaded' or 'online'"
            )
    
    def save_policy_file(self, file: UploadFile, policy_name: str) -> Tuple[str, str]:
        """Save policy file and return path and filename"""
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{policy_name.replace(' ', '_')}{file_extension}"
        file_path = self.upload_dir / file_name
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return str(file_path), file_name
    
    def create_policy(
        self,
        db: Session,
        policy_name: str,
        type: str,
        content: Optional[str] = None,
        file: Optional[UploadFile] = None,
        actions: Optional[bool] = None
    ) -> models.Policy:
        """Create a new policy"""
        policy_type = self.validate_policy_type(type)
        
        if policy_type == models.PolicyType.UPLOADED:
            if not file:
                raise HTTPException(
                    status_code=400, 
                    detail="File is required for uploaded policy type"
                )
            
            file_path, file_name = self.save_policy_file(file, policy_name)
            
            policy_data = {
                "policy_name": policy_name,
                "type": policy_type,
                "file_path": file_path,
                "file_name": file_name,
                "actions": actions
            }
        
        elif policy_type == models.PolicyType.ONLINE:
            if not content:
                raise HTTPException(
                    status_code=400, 
                    detail="Content is required for online policy type"
                )
            
            policy_data = {
                "policy_name": policy_name,
                "type": policy_type,
                "content": content,
                "actions": actions
            }
        
        return self.repository.create(db, policy_data)
    
    def get_all_policies(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Policy]:
        """Get all policies with pagination"""
        return self.repository.get_all(db, skip, limit)
    
    def get_policy_by_id(self, db: Session, policy_id: int) -> models.Policy:
        """Get policy by ID"""
        policy = self.repository.get_by_id(db, policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return policy
    
    def update_policy(
        self,
        db: Session,
        policy_id: int,
        policy_name: Optional[str] = None,
        type: Optional[str] = None,
        content: Optional[str] = None,
        file: Optional[UploadFile] = None,
        actions: Optional[bool] = None
    ) -> models.Policy:
        """Update an existing policy"""
        policy = self.get_policy_by_id(db, policy_id)
        
        update_data = {}
        
        # Update policy name if provided
        if policy_name is not None and policy_name.strip():
            update_data["policy_name"] = policy_name.strip()
            policy.policy_name = policy_name.strip()
        
        # Determine target type
        target_type = None
        if type:
            target_type = self.validate_policy_type(type)
        
        # Handle type change or updates
        if target_type == models.PolicyType.UPLOADED:
            if file:
                # Delete old file if exists
                if policy.file_path and os.path.exists(policy.file_path):
                    try:
                        os.remove(policy.file_path)
                    except Exception:
                        pass
                
                # Save new file
                file_path, file_name = self.save_policy_file(file, policy.policy_name)
                update_data["file_path"] = file_path
                update_data["file_name"] = file_name
                update_data["content"] = None
            elif policy.type != models.PolicyType.UPLOADED:
                raise HTTPException(
                    status_code=400,
                    detail="File is required when changing to uploaded policy type"
                )
            
            update_data["type"] = models.PolicyType.UPLOADED
        
        elif target_type == models.PolicyType.ONLINE:
            if content is not None:
                update_data["content"] = content
                
                # Delete file if switching from uploaded to online
                if policy.file_path and os.path.exists(policy.file_path):
                    try:
                        os.remove(policy.file_path)
                    except Exception:
                        pass
                
                update_data["file_path"] = None
                update_data["file_name"] = None
            elif policy.type != models.PolicyType.ONLINE:
                raise HTTPException(
                    status_code=400,
                    detail="Content is required when changing to online policy type"
                )
            
            update_data["type"] = models.PolicyType.ONLINE
        
        else:
            # No type change, just update existing policy's content/file
            if policy.type == models.PolicyType.UPLOADED and file:
                if policy.file_path and os.path.exists(policy.file_path):
                    try:
                        os.remove(policy.file_path)
                    except Exception:
                        pass
                
                file_path, file_name = self.save_policy_file(file, policy.policy_name)
                update_data["file_path"] = file_path
                update_data["file_name"] = file_name
            
            elif policy.type == models.PolicyType.ONLINE and content is not None:
                update_data["content"] = content
        
        if actions is not None:
            update_data["actions"] = actions
        
        return self.repository.update(db, policy, update_data)
    
    def delete_policy(self, db: Session, policy_id: int) -> dict:
        """Delete a policy"""
        policy = self.get_policy_by_id(db, policy_id)
        policy_name = policy.policy_name
        self.repository.delete_with_file(db, policy)
        return {"message": f"Policy '{policy_name}' deleted successfully"}
    
    def get_policy_file_path(self, db: Session, policy_id: int) -> Tuple[str, str]:
        """Get policy file path for download"""
        policy = self.get_policy_by_id(db, policy_id)
        
        if policy.type != models.PolicyType.UPLOADED or not policy.file_path:
            raise HTTPException(
                status_code=400, 
                detail="This policy does not have a downloadable file"
            )
        
        if not os.path.exists(policy.file_path):
            raise HTTPException(
                status_code=404, 
                detail="Policy file not found on server"
            )
        
        return policy.file_path, policy.file_name