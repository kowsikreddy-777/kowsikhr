from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import models
from app.schemas import BirthdayGreetingBase, BirthdayGreetingResponse

router = APIRouter(
    prefix="/birthday",
    tags=["Birthday Greetings"]
)

# ✅ Create multiple birthday greetings 
@router.post("/", response_model=BirthdayGreetingResponse)
def create_birthday_greeting(data: BirthdayGreetingBase, db: Session = Depends(get_db)):
    new_setting = models.BirthdayGreeting(**data.dict())
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    return new_setting


# Get all birthday greetings
@router.get("/", response_model=list[BirthdayGreetingResponse])
def get_all_birthday_greetings(db: Session = Depends(get_db)):
    return db.query(models.BirthdayGreeting).all()


# Get a specific birthday greeting by ID
@router.get("/{id}", response_model=BirthdayGreetingResponse)
def get_birthday_greeting(id: int, db: Session = Depends(get_db)):
    greeting = db.query(models.BirthdayGreeting).filter(
        models.BirthdayGreeting.id == id
    ).first()
    if not greeting:
        raise HTTPException(status_code=404, detail="Birthday greeting not found")
    return greeting


# Update a birthday greeting
@router.put("/{id}", response_model=BirthdayGreetingResponse)
def update_birthday_greeting(id: int, data: BirthdayGreetingBase, db: Session = Depends(get_db)):
    greeting = db.query(models.BirthdayGreeting).filter(
        models.BirthdayGreeting.id == id
    ).first()
    if not greeting:
        raise HTTPException(status_code=404, detail="Birthday greeting not found")

    for key, value in data.dict().items():
        setattr(greeting, key, value)

    db.commit()
    db.refresh(greeting)
    return greeting


# Delete a birthday greeting
@router.delete("/{id}")
def delete_birthday_greeting(id: int, db: Session = Depends(get_db)):
    greeting = db.query(models.BirthdayGreeting).filter(
        models.BirthdayGreeting.id == id
    ).first()
    if not greeting:
        raise HTTPException(status_code=404, detail="Birthday greeting not found")

    db.delete(greeting)
    db.commit()
    return {"message": f"Birthday greeting {id} deleted successfully"}
