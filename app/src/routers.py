from fastapi import APIRouter

from presentation.http.v1.handlers.admin import router as admin_router
from presentation.http.v1.handlers.auth import router as auth_router
from presentation.http.v1.handlers.users import router as users_router
from presentation.http.v1.handlers.webhooks import router as webhooks_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(admin_router)
api_router.include_router(webhooks_router)
