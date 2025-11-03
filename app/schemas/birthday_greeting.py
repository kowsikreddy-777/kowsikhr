from pydantic import BaseModel


class BirthdayGreetingBase(BaseModel):
    enable: bool = True
    send_copy: bool = True
    post_feed: bool = True
    search_employee: str | None = None
    message: str | None = None


class BirthdayGreetingResponse(BirthdayGreetingBase):
    id: int
    
    class Config:
        from_attributes = True
