from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# 📨 Letter Template Schema
class LetterTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_offer_letter: bool = False


class LetterTemplateCreate(LetterTemplateBase):
    pass


class LetterTemplateResponse(LetterTemplateBase):
    id: int
    file_path: str
    last_updated: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (was orm_mode in v1)


# 📜 Letter History Schema
class LetterHistoryBase(BaseModel):
    letter_name: str
    status: Optional[str] = "Completed"


class LetterHistoryCreate(LetterHistoryBase):
    pass


class LetterHistoryResponse(LetterHistoryBase):
    id: int
    requested_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (was orm_mode in v1)