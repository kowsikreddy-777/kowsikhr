"""
Notification Service - Business Logic Layer for Notifications
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import os
from fastapi import HTTPException, UploadFile

from app.repositories.notification_repository import NotificationRepository
from app import models


class NotificationService:
    """Service for Notification business logic"""
    
    def __init__(self):
        self.repository = NotificationRepository()
        self.upload_dir = Path("uploads/notifications")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_send_option(self, send_option: str) -> models.SendOption:
        """Validate and convert send option"""
        try:
            return models.SendOption(send_option)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid send option. Use 'send_now' or 'send_later'"
            )
    
    def parse_scheduled_time(self, scheduled_time: Optional[str]) -> Optional[datetime]:
        """Parse scheduled time from string"""
        if not scheduled_time:
            return None
        
        try:
            return datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid scheduled_time format. Use ISO format."
            )
    
    def validate_image(self, image: UploadFile) -> bytes:
        """Validate image file"""
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(
                status_code=400, 
                detail="Only JPG, JPEG, PNG images are allowed"
            )
        
        return image.file.read()
    
    def save_image(self, image: UploadFile, subject: str) -> Tuple[str, str]:
        """Save image file and return path and filename"""
        file_content = self.validate_image(image)
        
        if len(file_content) > 1_000_000:  # 1MB
            raise HTTPException(
                status_code=400, 
                detail="Image size must be less than 1MB"
            )
        
        file_extension = os.path.splitext(image.filename)[1]
        safe_subject = subject.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
        image_filename = f"{safe_subject}_{datetime.now().timestamp()}{file_extension}"
        image_path_obj = self.upload_dir / image_filename
        
        with open(image_path_obj, "wb") as buffer:
            buffer.write(file_content)
        
        return str(image_path_obj), image_filename
    
    def create_notification(
        self,
        db: Session,
        location: str,
        department: str,
        send_option: str,
        subject: str,
        description: str,
        employee_search: Optional[str] = None,
        scheduled_time: Optional[str] = None,
        image: Optional[UploadFile] = None
    ) -> models.Notification:
        """Create a new notification"""
        # Validate send option
        send_opt = self.validate_send_option(send_option)
        
        # Parse scheduled time
        scheduled_dt = self.parse_scheduled_time(scheduled_time)
        
        # Validate send_later requires scheduled_time
        if send_opt == models.SendOption.SEND_LATER and not scheduled_dt:
            raise HTTPException(
                status_code=400, 
                detail="scheduled_time is required when send_option is 'send_later'"
            )
        
        # Handle image upload
        image_path = None
        image_filename = None
        
        if image:
            image_path, image_filename = self.save_image(image, subject)
        
        # Create notification
        notification_data = {
            "location": location,
            "department": department,
            "employee_search": employee_search,
            "send_option": send_opt,
            "subject": subject,
            "description": description,
            "image_path": image_path,
            "image_filename": image_filename,
            "scheduled_time": scheduled_dt,
            "is_sent": (send_opt == models.SendOption.SEND_NOW),
            "sent_at": datetime.now() if send_opt == models.SendOption.SEND_NOW else None
        }
        
        return self.repository.create(db, notification_data)
    
    def get_all_notifications(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        location: Optional[str] = None,
        department: Optional[str] = None,
        is_sent: Optional[bool] = None
    ) -> List[models.Notification]:
        """Get all notifications with optional filters"""
        return self.repository.get_all_with_filters(
            db, skip, limit, location, department, is_sent
        )
    
    def get_notification_by_id(self, db: Session, notification_id: int) -> models.Notification:
        """Get notification by ID"""
        notification = self.repository.get_by_id(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification
    
    def update_notification(
        self,
        db: Session,
        notification_id: int,
        location: Optional[str] = None,
        department: Optional[str] = None,
        send_option: Optional[str] = None,
        subject: Optional[str] = None,
        description: Optional[str] = None,
        employee_search: Optional[str] = None,
        scheduled_time: Optional[str] = None,
        image: Optional[UploadFile] = None
    ) -> models.Notification:
        """Update an existing notification"""
        notification = self.get_notification_by_id(db, notification_id)
        
        update_data = {}
        
        if location:
            update_data["location"] = location
        if department:
            update_data["department"] = department
        if employee_search is not None:
            update_data["employee_search"] = employee_search
        if subject:
            update_data["subject"] = subject
        if description:
            update_data["description"] = description
        
        # Handle send option change
        if send_option:
            send_opt = self.validate_send_option(send_option)
            update_data["send_option"] = send_opt
        
        # Handle scheduled time
        if scheduled_time:
            scheduled_dt = self.parse_scheduled_time(scheduled_time)
            update_data["scheduled_time"] = scheduled_dt
        
        # Handle image update
        if image:
            # Delete old image if exists
            if notification.image_path and os.path.exists(notification.image_path):
                try:
                    os.remove(notification.image_path)
                except Exception:
                    pass
            
            image_path, image_filename = self.save_image(image, notification.subject)
            update_data["image_path"] = image_path
            update_data["image_filename"] = image_filename
        
        return self.repository.update(db, notification, update_data)
    
    def delete_notification(self, db: Session, notification_id: int) -> dict:
        """Delete a notification"""
        notification = self.get_notification_by_id(db, notification_id)
        subject = notification.subject
        self.repository.delete_with_image(db, notification)
        return {"message": f"Notification '{subject}' deleted successfully"}
    
    def get_notification_image_path(self, db: Session, notification_id: int) -> str:
        """Get notification image path"""
        notification = self.get_notification_by_id(db, notification_id)
        
        if not notification.image_path:
            raise HTTPException(
                status_code=404, 
                detail="This notification does not have an image"
            )
        
        if not os.path.exists(notification.image_path):
            raise HTTPException(
                status_code=404, 
                detail="Image file not found on server"
            )
        
        return notification.image_path
    
    def send_notification(self, db: Session, notification_id: int) -> dict:
        """Manually trigger sending a notification"""
        notification = self.get_notification_by_id(db, notification_id)
        
        if notification.is_sent:
            raise HTTPException(
                status_code=400, 
                detail="Notification already sent"
            )
        
        # Mark as sent
        notification = self.repository.mark_as_sent(db, notification)
        
        return {
            "message": "Notification sent successfully",
            "notification_id": notification.id,
            "sent_at": notification.sent_at
        }
    
    def get_notification_stats(self, db: Session) -> dict:
        """Get notification statistics"""
        return self.repository.get_stats(db)