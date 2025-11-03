from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.database import SessionLocal

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# CRUD OPERATIONS FOR ALERTS
# ------------------------------

@router.get("/", response_model=list[schemas.Alert])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()


@router.get("/{alert_id}", response_model=schemas.Alert)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.put("/{alert_id}", response_model=schemas.Alert)
def update_alert(alert_id: int, alert: schemas.AlertUpdate, db: Session = Depends(get_db)):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    for key, value in alert.dict().items():
        setattr(db_alert, key, value)

    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(db_alert)
    db.commit()
    return {"message": "Alert deleted successfully"}
    