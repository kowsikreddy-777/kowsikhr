from fastapi import APIRouter

from app.api.v1 import (
    birthday,
    work_anniversary,
    wedding_anniversary,
    notification,
    policy,
    alert,
    letter,
)


api_router = APIRouter(prefix="/api/v1")


api_router.include_router(birthday.router)
api_router.include_router(work_anniversary.router)
api_router.include_router(wedding_anniversary.router)
api_router.include_router(policy.router)
api_router.include_router(notification.router)
api_router.include_router(alert.router)
api_router.include_router(letter.router)