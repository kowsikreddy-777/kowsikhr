from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import models  # Changed this line
from app.schemas import WeddingAnniversaryGreetingBase, WeddingAnniversaryGreetingResponse

router = APIRouter(
    prefix="/wedding",
    tags=["Wedding Anniversary Greetings"]
)


@router.post("/", response_model=WeddingAnniversaryGreetingResponse)
def create_wedding_greeting(data: WeddingAnniversaryGreetingBase, db: Session = Depends(get_db)):
    new = models.WeddingAnniversaryGreeting(**data.dict())  # Changed
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/", response_model=list[WeddingAnniversaryGreetingResponse])
def get_all_wedding_greetings(db: Session = Depends(get_db)):
    return db.query(models.WeddingAnniversaryGreeting).all()  # Changed


@router.get("/{id}", response_model=WeddingAnniversaryGreetingResponse)
def get_wedding_greeting(id: int, db: Session = Depends(get_db)):
    greeting = db.query(models.WeddingAnniversaryGreeting).filter(
        models.WeddingAnniversaryGreeting.id == id
    ).first()  # Changed
    if not greeting:
        raise HTTPException(status_code=404, detail="Wedding anniversary greeting not found")
    return greeting


@router.put("/{id}", response_model=WeddingAnniversaryGreetingResponse)
def update_wedding_greeting(id: int, data: WeddingAnniversaryGreetingBase, db: Session = Depends(get_db)):
    greeting = db.query(models.WeddingAnniversaryGreeting).filter(
        models.WeddingAnniversaryGreeting.id == id
    ).first()  # Changed
    if not greeting:
        raise HTTPException(status_code=404, detail="Wedding anniversary greeting not found")
    for key, value in data.dict().items():
        setattr(greeting, key, value)
    db.commit()
    db.refresh(greeting)
    return greeting


@router.delete("/{id}")
def delete_wedding_greeting(id: int, db: Session = Depends(get_db)):
    greeting = db.query(models.WeddingAnniversaryGreeting).filter(
        models.WeddingAnniversaryGreeting.id == id
    ).first()  # Changed
    if not greeting:
        raise HTTPException(status_code=404, detail="Wedding anniversary greeting not found")
    db.delete(greeting)
    db.commit()
    return {"message": f"Wedding anniversary greeting {id} deleted successfully"}