"""
Alert Repository - Data Access Layer for Alerts
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models


class AlertRepository:
    """Repository for Alert model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Alert]:
        """Get all alerts with pagination"""
        return db.query(models.Alert).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, alert_id: int) -> Optional[models.Alert]:
        """Get alert by ID"""
        return db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    
    def create(self, db: Session, alert_data: dict) -> models.Alert:
        """Create a new alert"""
        db_alert = models.Alert(**alert_data)
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
    
    def update(self, db: Session, alert: models.Alert, update_data: dict) -> models.Alert:
        """Update an existing alert"""
        for key, value in update_data.items():
            if value is not None:
                setattr(alert, key, value)
        db.commit()
        db.refresh(alert)
        return alert
    
    def delete(self, db: Session, alert: models.Alert) -> bool:
        """Delete an alert"""
        db.delete(alert)
        db.commit()
        return True
    
    def get_active_alerts(self, db: Session) -> List[models.Alert]:
        """Get all active alerts"""
        return db.query(models.Alert).filter(models.Alert.active == True).all()
    
    def get_by_name(self, db: Session, alert_name: str) -> Optional[models.Alert]:
        """Get alert by name"""
        return db.query(models.Alert).filter(models.Alert.alert_name == alert_name).first()