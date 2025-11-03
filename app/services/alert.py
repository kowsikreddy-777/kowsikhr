"""
Alert Service - Business Logic Layer for Alerts
"""
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.repositories.alert_repository import AlertRepository
from app import models, schemas


class AlertService:
    """Service for Alert business logic"""
    
    def __init__(self):
        self.repository = AlertRepository()
    
    def get_all_alerts(self, db: Session) -> List[models.Alert]:
        """Get all alerts"""
        return self.repository.get_all(db)
    
    def get_alert_by_id(self, db: Session, alert_id: int) -> models.Alert:
        """Get alert by ID"""
        alert = self.repository.get_by_id(db, alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    
    def create_alert(self, db: Session, alert_data: schemas.AlertCreate) -> models.Alert:
        """Create a new alert"""
        return self.repository.create(db, alert_data.dict())
    
    def update_alert(self, db: Session, alert_id: int, alert_data: schemas.AlertUpdate) -> models.Alert:
        """Update an existing alert"""
        alert = self.get_alert_by_id(db, alert_id)
        return self.repository.update(db, alert, alert_data.dict())
    
    def delete_alert(self, db: Session, alert_id: int) -> dict:
        """Delete an alert"""
        alert = self.get_alert_by_id(db, alert_id)
        self.repository.delete(db, alert)
        return {"message": "Alert deleted successfully"}
    
    def get_active_alerts(self, db: Session) -> List[models.Alert]:
        """Get all active alerts"""
        return self.repository.get_active_alerts(db)