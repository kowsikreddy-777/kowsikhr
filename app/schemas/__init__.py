from .work_anniversary import (
    WorkAnniversaryGreetingBase,
    WorkAnniversaryGreetingCreate,
    WorkAnniversaryGreetingResponse,
)
from .birthday_greeting import BirthdayGreetingBase, BirthdayGreetingResponse
from .wedding_anniversary import WeddingAnniversaryGreetingBase, WeddingAnniversaryGreetingResponse


from .notification import NotificationCreate, NotificationResponse,NotificationUpdate,NotificationListResponse,LocationList,DepartmentList



from .policy import PolicyCreate, PolicyResponse,PolicyListResponse


from .alert import Alert, AlertCreate, AlertUpdate, AlertBase

from app.schemas.letter import (
       LetterTemplateResponse,
       LetterHistoryResponse,
       # ... other classes
   )