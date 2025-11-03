from sqlalchemy import Column, Integer, Boolean, String
from app.core.database import Base


# ------------------------------------
# Models
# ------------------------------------
class BirthdayGreeting(Base):
    __tablename__ = "birthday_greetings"
    
    id = Column(Integer, primary_key=True, index=True)
    enable = Column(Boolean, default=True)
    send_copy = Column(Boolean, default=True)
    post_feed = Column(Boolean, default=True)
    search_employee=Column(String, nullable=True)
    message = Column(String, nullable=True)


