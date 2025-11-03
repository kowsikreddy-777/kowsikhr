from sqlalchemy import Column, Integer, Boolean, String
from app.core.database import Base


# ------------------------------------
# Models
# ------------------------------------

class WeddingAnniversaryGreeting(Base):
    __tablename__ = "wedding_anniversary_greetings"
    
    id = Column(Integer, primary_key=True, index=True)
    enable = Column(Boolean, default=False)
    send_copy = Column(Boolean, default=True)
    post_feed = Column(Boolean, default=True)
    subject = Column(String, nullable=True)
    message = Column(String, nullable=True)