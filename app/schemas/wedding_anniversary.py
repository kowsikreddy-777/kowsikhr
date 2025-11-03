from pydantic import BaseModel

class WeddingAnniversaryGreetingBase(BaseModel):
    enable: bool = False
    send_copy: bool = True
    post_feed: bool = True
    subject: str | None = None
    message: str | None = None


class WeddingAnniversaryGreetingResponse(WeddingAnniversaryGreetingBase):
    id: int
    
    class Config:
        from_attributes = True