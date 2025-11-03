"""
Notification Router - All CRUD Operations for Notifications
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from datetime import datetime
from datetime import datetime, timezone

import shutil
import os
from sqlalchemy import func


from app.core.database import get_db
from app import models  # Changed this line
from app.schemas import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationListResponse,
    LocationList,
    DepartmentList
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

# Directory for storing notification images
UPLOAD_DIR = Path("uploads/notifications")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=NotificationResponse, status_code=201)
async def create_notification(
    location: str = Form(...),
    department: str = Form(...),
    send_option: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    employee_search: Optional[str] = Form(None),
    scheduled_time: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    
    # Validate send option
    try:
        send_opt = models.SendOption(send_option)  # Changed
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid send option. Use 'send_now' or 'send_later'")
    
    # Parse scheduled time if provided
    scheduled_dt = None
    if scheduled_time:
        try:
            scheduled_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid scheduled_time format. Use ISO format.")
    
    # Validate send_later requires scheduled_time
    if send_opt == models.SendOption.SEND_LATER and not scheduled_dt:  # Changed
        raise HTTPException(status_code=400, detail="scheduled_time is required when send_option is 'send_later'")
    
    # Handle image upload
    image_path = None
    image_filename = None
    
    if image:
        # Validate image
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPG, JPEG, PNG images are allowed")
        
        # Check file size (max 1MB)
        file_content = await image.read()
        if len(file_content) > 1_000_000:  # 1MB in bytes
            raise HTTPException(status_code=400, detail="Image size must be less than 1MB")
        
        # Save image
        file_extension = os.path.splitext(image.filename)[1]
        safe_subject = subject.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
        image_filename = f"{safe_subject}_{datetime.now().timestamp()}{file_extension}"
        image_path_obj = UPLOAD_DIR / image_filename
        
        with open(image_path_obj, "wb") as buffer:
            buffer.write(file_content)
        
        image_path = str(image_path_obj)
    
    # Create notification
    new_notification = models.Notification(  # Changed
        location=location,
        department=department,
        employee_search=employee_search,
        send_option=send_opt,
        subject=subject,
        description=description,
        image_path=image_path,
        image_filename=image_filename,
        scheduled_time=scheduled_dt,
        is_sent=(send_opt == models.SendOption.SEND_NOW),  # Changed
        sent_at=datetime.now() if send_opt == models.SendOption.SEND_NOW else None  # Changed
    )
    
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


# @router.get("/", response_model=List[NotificationListResponse])
# def get_all_notifications(
#     skip: int = 0,
#     limit: int = 100,
#     location: Optional[str] = None,
#     department: Optional[str] = None,
#     is_sent: Optional[bool] = None,
#     db: Session = Depends(get_db)
# ):
   
#     query = db.query(models.Notification)  # Changed
    
#     if location:
#         query = query.filter(models.Notification.location == location)  # Changed
    
#     if department:
#         query = query.filter(models.Notification.department == department)  # Changed
    
#     if is_sent is not None:
#         query = query.filter(models.Notification.is_sent == is_sent)  # Changed
    
#     notifications = query.order_by(models.Notification.created_at.desc()).offset(skip).limit(limit).all()  # Changed
#     return notifications

@router.get("/", response_model=List[NotificationListResponse])
def get_all_notifications(db: Session = Depends(get_db)):
    notifications = (
        db.query(models.Notification)
        .order_by(models.Notification.created_at.desc())
        .all()
    )
    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()  # Changed
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    location: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    send_option: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    employee_search: Optional[str] = Form(None),
    scheduled_time: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()  # Changed
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Update fields if provided
    if location:
        notification.location = location
    if department:
        notification.department = department
    if employee_search is not None:
        notification.employee_search = employee_search
    if subject:
        notification.subject = subject
    if description:
        notification.description = description
    
    # Handle send option change
    if send_option:
        try:
            send_opt = models.SendOption(send_option)  # Changed
            notification.send_option = send_opt
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid send option")
    
    # Handle scheduled time
    if scheduled_time:
        try:
            scheduled_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
            notification.scheduled_time = scheduled_dt
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid scheduled_time format")
    
    # Handle image update
    if image:
        # Delete old image if exists
        if notification.image_path and os.path.exists(notification.image_path):
            try:
                os.remove(notification.image_path)
            except Exception:
                pass
        
        # Validate and save new image
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPG, JPEG, PNG images are allowed")
        
        file_content = await image.read()
        if len(file_content) > 1_000_000:
            raise HTTPException(status_code=400, detail="Image size must be less than 1MB")
        
        file_extension = os.path.splitext(image.filename)[1]
        safe_subject = notification.subject.replace(' ', '_')[:50]
        image_filename = f"{safe_subject}_{datetime.now().timestamp()}{file_extension}"
        image_path_obj = UPLOAD_DIR / image_filename
        
        with open(image_path_obj, "wb") as buffer:
            buffer.write(file_content)
        
        notification.image_path = str(image_path_obj)
        notification.image_filename = image_filename
    
    db.commit()
    db.refresh(notification)
    return notification


@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()  # Changed
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Delete associated image if exists
    if notification.image_path and os.path.exists(notification.image_path):
        try:
            os.remove(notification.image_path)
        except Exception:
            pass
    
    subject = notification.subject
    db.delete(notification)
    db.commit()
    return {"message": f"Notification '{subject}' deleted successfully"}


@router.get("/{notification_id}/image")
def get_notification_image(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()  # Changed
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if not notification.image_path:
        raise HTTPException(status_code=404, detail="This notification does not have an image")
    
    if not os.path.exists(notification.image_path):
        raise HTTPException(status_code=404, detail="Image file not found on server")
    
    return FileResponse(
        path=notification.image_path,
        filename=notification.image_filename,
        media_type='image/jpeg'
    )




# @router.post("/{notification_id}/send")
# def send_notification_now(notification_id: int, db: Session = Depends(get_db)):
    
#     notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()  # Changed
#     if not notification:
#         raise HTTPException(status_code=404, detail="Notification not found")
    
#     if notification.is_sent:
#         raise HTTPException(status_code=400, detail="Notification already sent")
   
#     # Mark as sent
#     notification.is_sent = True
#     notification.sent_at = datetime.now()
    
#     db.commit()
#     db.refresh(notification)
    
#     return {
#         "message": "Notification sent successfully",
#         "notification_id": notification.id,
#         "sent_at": notification.sent_at
#     }


@router.get("/stats/summary")
def get_notification_stats(db: Session = Depends(get_db)):
    # Overall counts
    total_notifications = db.query(models.Notification).count()
    sent_notifications = db.query(models.Notification).filter(models.Notification.is_sent == True).count()
    pending_notifications = db.query(models.Notification).filter(models.Notification.is_sent == False).count()

    # Count by location (dynamic)
    location_counts = (
        db.query(models.Notification.location, func.count(models.Notification.id))
        .group_by(models.Notification.location)
        .all()
    )
    by_location = {loc or "Unknown": count for loc, count in location_counts}

    # Count by department (dynamic)
    department_counts = (
        db.query(models.Notification.department, func.count(models.Notification.id))
        .group_by(models.Notification.department)
        .all()
    )
    by_department = {dept or "Unknown": count for dept, count in department_counts}

    return {
        "total_notifications": total_notifications,
        "sent_notifications": sent_notifications,
        "pending_notifications": pending_notifications,
        "by_location": by_location,
        "by_department": by_department
    }




# @router.get("/stats/summary")
# def get_notification_stats(db: Session = Depends(get_db)):
    
#     total_notifications = db.query(models.Notification).count()  # Changed
#     sent_notifications = db.query(models.Notification).filter(models.Notification.is_sent == True).count()  # Changed
#     pending_notifications = db.query(models.Notification).filter(models.Notification.is_sent == False).count()  # Changed
    
#     # Count by location
#     bangalore = db.query(models.Notification).filter(models.Notification.location == "bangalore").count()  # Changed
#     hyderabad = db.query(models.Notification).filter(models.Notification.location == "hyderabad").count()  # Changed
#     all_locations = db.query(models.Notification).filter(models.Notification.location == "all_locations").count()  # Changed
    
#     # Count by department
#     product_dev = db.query(models.Notification).filter(models.Notification.department == "product_development").count()  # Changed
#     hr_exec = db.query(models.Notification).filter(models.Notification.department == "hr_executive").count()  # Changed
#     tech_support = db.query(models.Notification).filter(models.Notification.department == "technical_support").count()  # Changed
#     all_departments = db.query(models.Notification).filter(models.Notification.department == "all_departments").count()  # Changed
    
#     return {
#         "total_notifications": total_notifications,
#         "sent_notifications": sent_notifications,
#         "pending_notifications": pending_notifications,
#         "by_location": {
#             "all_locations": all_locations,
#             "bangalore": bangalore,
#             "hyderabad": hyderabad
#         },
#         "by_department": {
#             "all_departments": all_departments,
#             "product_development": product_dev,
#             "hr_executive": hr_exec,
#             "technical_support": tech_support
#         }
#     }