from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import models
from app.schemas import WorkAnniversaryGreetingCreate, WorkAnniversaryGreetingResponse

router = APIRouter(
    prefix="/work",
    tags=["Work Anniversary Greetings"],
)

# ✅ Create a single greeting
@router.post("/", response_model=WorkAnniversaryGreetingResponse)
def create_work_anniversary_greeting(
    data: WorkAnniversaryGreetingCreate,
    db: Session = Depends(get_db),
):
    
    db_greeting = models.WorkAnniversaryGreeting(**data.dict())
    db.add(db_greeting)
    db.commit()
    db.refresh(db_greeting)
    return db_greeting

# ✅ Get all greetings
@router.get("/", response_model=list[WorkAnniversaryGreetingResponse])
def get_all_work_anniversary_greetings(db: Session = Depends(get_db)):
    
    return db.query(models.WorkAnniversaryGreeting).all()

# ✅ Get greeting by ID
@router.get("/{id}", response_model=WorkAnniversaryGreetingResponse)
def get_work_anniversary_greeting(id: int, db: Session = Depends(get_db)):
    
    greeting = db.query(models.WorkAnniversaryGreeting).filter(models.WorkAnniversaryGreeting.id == id).first()
    if not greeting:
        raise HTTPException(status_code=404, detail="Greeting not found")
    return greeting

# ✅ Update greeting by ID
@router.put("/{id}", response_model=WorkAnniversaryGreetingResponse)
def update_work_anniversary_greeting(
    id: int,
    data: WorkAnniversaryGreetingCreate,
    db: Session = Depends(get_db),
):
    
    greeting = db.query(models.WorkAnniversaryGreeting).filter(models.WorkAnniversaryGreeting.id == id).first()
    if not greeting:
        raise HTTPException(status_code=404, detail="Greeting not found")

    for key, value in data.dict().items():
        setattr(greeting, key, value)

    db.commit()
    db.refresh(greeting)
    return greeting

# ✅ Delete greeting by ID
@router.delete("/{id}")
def delete_work_anniversary_greeting(id: int, db: Session = Depends(get_db)):
    
    greeting = db.query(models.WorkAnniversaryGreeting).filter(models.WorkAnniversaryGreeting.id == id).first()
    if not greeting:
        raise HTTPException(status_code=404, detail="Greeting not found")

    db.delete(greeting)
    db.commit()
    return {"message": f"Greeting {id} deleted successfully"}
