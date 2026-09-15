from fastapi import APIRouter, Depends

from app.api.dependencies import current_user
from app.services.stats import build_dashboard, build_progress

router = APIRouter(tags=["Stats"])


@router.get("/dashboard")
async def get_dashboard(user: dict = Depends(current_user)) -> dict:
    return await build_dashboard(user["id"])


@router.get("/progress")
async def get_progress(user: dict = Depends(current_user)) -> dict:
    return await build_progress(user["id"])