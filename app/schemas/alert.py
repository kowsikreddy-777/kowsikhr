from pydantic import BaseModel

class AlertBase(BaseModel):
    alert_name: str
    attendance_condition: str
    days_more_than: int
    send_letter: str
    check_every: str
    active: bool

class AlertCreate(AlertBase):
    pass

class AlertUpdate(AlertBase):
    pass

class Alert(AlertBase):
    id: int

    class Config:
        from_attributes = True
