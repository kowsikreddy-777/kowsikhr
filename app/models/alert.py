from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_name = Column(String, index=True)
    attendance_condition = Column(String)
    days_more_than = Column(Integer)
    send_letter = Column(String)
    check_every = Column(String)
    active = Column(Boolean, default=True)
