from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.database import get_db
from pathlib import Path
import shutil
from datetime import datetime


router = APIRouter(prefix="/letters", tags=["Letters"])

UPLOAD_DIR = Path("uploaded_letters")
UPLOAD_DIR.mkdir(exist_ok=True)


# ✅ READ ALL LETTERS
@router.get("/", response_model=list[schemas.LetterTemplateResponse])
def list_letters(db: Session = Depends(get_db)):
    return db.query(models.LetterTemplate).all()


# ✅ CREATE LETTER TEMPLATE (Allow any file type)
@router.post("/", response_model=schemas.LetterTemplateResponse)
async def create_letter(
    name: str = Form(...),
    description: str = Form(None),
    is_offer_letter: bool = Form(False),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Allow any file type
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    letter = models.LetterTemplate(
        name=name,
        description=description,
        is_offer_letter=is_offer_letter,
        file_path=str(file_path),
        last_updated=datetime.utcnow()
    )

    db.add(letter)
    db.commit()
    db.refresh(letter)
    return letter


# ✅ UPDATE LETTER TEMPLATE (Allow any file type)
@router.put("/{letter_id}", response_model=schemas.LetterTemplateResponse)
async def update_letter(
    letter_id: int,
    name: str = Form(None),
    description: str = Form(None),
    is_offer_letter: bool = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    letter = db.query(models.LetterTemplate).filter(models.LetterTemplate.id == letter_id).first()
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")

    if name:
        letter.name = name
    if description:
        letter.description = description
    if is_offer_letter is not None:
        letter.is_offer_letter = is_offer_letter

    if file:
        # Allow any file type
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        letter.file_path = str(file_path)

    letter.last_updated = datetime.utcnow()

    db.commit()
    db.refresh(letter)
    return letter


# ✅ DELETE LETTER TEMPLATE
@router.delete("/{letter_id}")
def delete_letter(letter_id: int, db: Session = Depends(get_db)):
    letter = db.query(models.LetterTemplate).filter(models.LetterTemplate.id == letter_id).first()
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")

    # delete the file from the disk if exists
    try:
        if Path(letter.file_path).exists():
            Path(letter.file_path).unlink()
    except Exception:
        pass

    db.delete(letter)
    db.commit()
    return {"message": f"Letter '{letter.name}' deleted successfully"}


# ✅ LETTER HISTORY LIST
@router.get("/history", response_model=list[schemas.LetterHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.LetterHistory).order_by(models.LetterHistory.requested_at.desc()).all()


# ✅ GENERATE LETTER (simulated)
@router.post("/{letter_id}/generate")
def generate_letter(letter_id: int, db: Session = Depends(get_db)):
    letter = db.query(models.LetterTemplate).filter(models.LetterTemplate.id == letter_id).first()
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")

    history = models.LetterHistory(
        letter_name=letter.name,
        status="Completed"
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return {"message": f"Letter '{letter.name}' generated successfully", "history_id": history.id}


# ✅ DOWNLOAD LETTER TEMPLATE FILE
@router.get("/{letter_id}/download")
async def download_letter(
    letter_id: int,
    db: Session = Depends(get_db)
):
    letter = db.query(models.LetterTemplate).filter(models.LetterTemplate.id == letter_id).first()
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    
    file_path = Path(letter.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream"
    )