"""
Notification Repository - Data Access Layer for Notifications
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
import os
from app import models


class NotificationRepository:
    """Repository for Notification model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Notification]:
        """Get all notifications with pagination"""
        return db.query(models.Notification).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, notification_id: int) -> Optional[models.Notification]:
        """Get notification by ID"""
        return db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    
    def create(self, db: Session, notification_data: dict) -> models.Notification:
        """Create a new notification"""
        db_notification = models.Notification(**notification_data)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    
    def update(self, db: Session, notification: models.Notification, update_data: dict) -> models.Notification:
        """Update an existing notification"""
        for key, value in update_data.items():
            if value is not None:
                setattr(notification, key, value)
        db.commit()
        db.refresh(notification)
        return notification
    
    def delete(self, db: Session, notification: models.Notification) -> bool:
        """Delete a notification"""
        db.delete(notification)
        db.commit()
        return True
    
    def get_all_with_filters(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        location: Optional[str] = None,
        department: Optional[str] = None,
        is_sent: Optional[bool] = None
    ) -> List[models.Notification]:
        """Get notifications with optional filters"""
        query = db.query(models.Notification)
        
        if location:
            query = query.filter(models.Notification.location == location)
        
        if department:
            query = query.filter(models.Notification.department == department)
        
        if is_sent is not None:
            query = query.filter(models.Notification.is_sent == is_sent)
        
        return query.order_by(desc(models.Notification.created_at)).offset(skip).limit(limit).all()
    
    def get_pending_notifications(self, db: Session) -> List[models.Notification]:
        """Get all pending (unsent) notifications"""
        return db.query(models.Notification).filter(
            models.Notification.is_sent == False
        ).all()
    
    def get_scheduled_notifications(self, db: Session) -> List[models.Notification]:
        """Get notifications scheduled for later"""
        return db.query(models.Notification).filter(
            models.Notification.send_option == models.SendOption.SEND_LATER,
            models.Notification.is_sent == False
        ).all()
    
    def mark_as_sent(self, db: Session, notification: models.Notification) -> models.Notification:
        """Mark notification as sent"""
        from datetime import datetime
        notification.is_sent = True
        notification.sent_at = datetime.now()
        db.commit()
        db.refresh(notification)
        return notification
    
    def get_stats(self, db: Session) -> dict:
        """Get notification statistics"""
        stats = {
            "total_notifications": db.query(models.Notification).count(),
            "sent_notifications": db.query(models.Notification).filter(
                models.Notification.is_sent == True
            ).count(),
            "pending_notifications": db.query(models.Notification).filter(
                models.Notification.is_sent == False
            ).count(),
            "by_location": {
                "all_locations": db.query(models.Notification).filter(
                    models.Notification.location == "all_locations"
                ).count(),
                "bangalore": db.query(models.Notification).filter(
                    models.Notification.location == "bangalore"
                ).count(),
                "hyderabad": db.query(models.Notification).filter(
                    models.Notification.location == "hyderabad"
                ).count()
            },
            "by_department": {
                "all_departments": db.query(models.Notification).filter(
                    models.Notification.department == "all_departments"
                ).count(),
                "product_development": db.query(models.Notification).filter(
                    models.Notification.department == "product_development"
                ).count(),
                "hr_executive": db.query(models.Notification).filter(
                    models.Notification.department == "hr_executive"
                ).count(),
                "technical_support": db.query(models.Notification).filter(
                    models.Notification.department == "technical_support"
                ).count()
            }
        }
        return stats
    
    def delete_with_image(self, db: Session, notification: models.Notification) -> bool:
        """Delete notification and associated image file"""
        # Delete associated image if exists
        if notification.image_path and os.path.exists(notification.image_path):
            try:
                os.remove(notification.image_path)
            except Exception:
                pass
        
        db.delete(notification)
        db.commit()
        return True