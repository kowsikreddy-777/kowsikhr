from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import shutil
import os

from app.core.database import get_db
from app.models import Policy, PolicyType
from app.schemas import PolicyResponse, PolicyListResponse

router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)

# Directory for storing uploaded policy files
UPLOAD_DIR = Path("uploads/policies")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=PolicyResponse, status_code=201)
async def create_policy(
    policy_name: str = Form(...),
    type: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    actions: Optional[bool] = Form(None),
    db: Session = Depends(get_db)
):
    
    # Convert string to PolicyType enum
    try:
        policy_type = PolicyType(type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid policy type. Use 'uploaded' or 'online'")
    
    # Validate based on type
    if policy_type == PolicyType.UPLOADED:
        if not file:
            raise HTTPException(status_code=400, detail="File is required for uploaded policy type")
        
        # Save the uploaded file
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{policy_name.replace(' ', '_')}{file_extension}"
        file_path = UPLOAD_DIR / file_name
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        new_policy = Policy(
            policy_name=policy_name,
            type=policy_type,
            file_path=str(file_path),
            file_name=file_name
        )
    
    elif policy_type == PolicyType.ONLINE:
        if not content:
            raise HTTPException(status_code=400, detail="Content is required for online policy type")
        
        new_policy = Policy(
            policy_name=policy_name,
            type=policy_type,
            content=content
        )
    
    else:
        raise HTTPException(status_code=400, detail="Invalid policy type")
    
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy


@router.get("/", response_model=List[PolicyListResponse])
def get_all_policies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    policies = db.query(Policy).offset(skip).limit(limit).all()
    return policies


@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: int,
    policy_name: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    actions: Optional[bool] = Form(None),
    db: Session = Depends(get_db)
):
    # Get existing policy
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    # Update policy name if provided
    if policy_name is not None and policy_name.strip():
        policy.policy_name = policy_name.strip()
    
    # Determine target type
    target_type = None
    if type:
        try:
            target_type = PolicyType(type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid policy type. Use 'uploaded' or 'online'")
    
    # Handle type change or updates
    if target_type == PolicyType.UPLOADED:
        # Switching to or updating uploaded policy
        if not file:
            # If no file provided but already uploaded type, that's OK (just updating name)
            if policy.type != PolicyType.UPLOADED:
                raise HTTPException(
                    status_code=400, 
                    detail="File is required when changing to uploaded policy type"
                )
        else:
            # Delete old file if exists
            if policy.file_path and os.path.exists(policy.file_path):
                try:
                    os.remove(policy.file_path)
                except Exception as e:
                    print(f"Warning: Could not delete old file: {e}")
            
            # Save new file
            file_extension = os.path.splitext(file.filename)[1]
            if not file_extension:
                file_extension = '.pdf'  # Default extension
            
            safe_name = policy.policy_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
            file_name = f"{safe_name}{file_extension}"
            file_path = UPLOAD_DIR / file_name
            
            # Handle duplicate filenames
            counter = 1
            while file_path.exists():
                file_name = f"{safe_name}_{counter}{file_extension}"
                file_path = UPLOAD_DIR / file_name
                counter += 1
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            policy.file_path = str(file_path)
            policy.file_name = file_name
            policy.content = None  # Clear content when switching to uploaded
        
        policy.type = PolicyType.UPLOADED
    
    elif target_type == PolicyType.ONLINE:
        # Switching to or updating online policy
        if not content:
            # If no content provided but already online type, that's OK (just updating name)
            if policy.type != PolicyType.ONLINE:
                raise HTTPException(
                    status_code=400,
                    detail="Content is required when changing to online policy type"
                )
        else:
            policy.content = content
            
            # Delete file if switching from uploaded to online
            if policy.file_path and os.path.exists(policy.file_path):
                try:
                    os.remove(policy.file_path)
                except Exception as e:
                    print(f"Warning: Could not delete old file: {e}")
            
            policy.file_path = None
            policy.file_name = None
        
        policy.type = PolicyType.ONLINE
    
    else:
        # No type change, just update existing policy's content/file
        if policy.type == PolicyType.UPLOADED and file:
            # Update file for uploaded policy
            if policy.file_path and os.path.exists(policy.file_path):
                try:
                    os.remove(policy.file_path)
                except Exception as e:
                    print(f"Warning: Could not delete old file: {e}")
            
            file_extension = os.path.splitext(file.filename)[1]
            if not file_extension:
                file_extension = '.pdf'
            
            safe_name = policy.policy_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
            file_name = f"{safe_name}{file_extension}"
            file_path = UPLOAD_DIR / file_name
            
            counter = 1
            while file_path.exists():
                file_name = f"{safe_name}_{counter}{file_extension}"
                file_path = UPLOAD_DIR / file_name
                counter += 1
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            policy.file_path = str(file_path)
            policy.file_name = file_name
        
        elif policy.type == PolicyType.ONLINE and content is not None:
            # Update content for online policy
            policy.content = content
    
    db.commit()
    db.refresh(policy)
    return policy

@router.delete("/{policy_id}")
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    # Delete associated file if exists
    if policy.file_path and os.path.exists(policy.file_path):
        os.remove(policy.file_path)
    
    db.delete(policy)
    db.commit()
    return {"message": f"Policy '{policy.policy_name}' deleted successfully"}


@router.get("/{policy_id}/download")
def download_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    if policy.type != PolicyType.UPLOADED or not policy.file_path:
        raise HTTPException(status_code=400, detail="This policy does not have a downloadable file")
    
    if not os.path.exists(policy.file_path):
        raise HTTPException(status_code=404, detail="Policy file not found on server")
    
    return FileResponse(
        path=policy.file_path,
        filename=policy.file_name,
        media_type='application/octet-stream'
    )