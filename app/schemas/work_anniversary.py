from pydantic import BaseModel



class WorkAnniversaryGreetingBase(BaseModel):
    enable: bool
    send_copy: bool
    post_feed: bool
    subject: str
    message: str

class WorkAnniversaryGreetingCreate(WorkAnniversaryGreetingBase):
    pass

class WorkAnniversaryGreetingResponse(WorkAnniversaryGreetingBase):
    id: int

    class Config:
        from_attributes = True

