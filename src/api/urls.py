from fastapi import APIRouter

from src.api.routes import task_manager

api_router = APIRouter()

api_router.include_router(task_manager.router, prefix="/task", tags=["tasks"])
