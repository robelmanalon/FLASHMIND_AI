import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import current_user
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services import decks as decks_service
from app.services import profiles as profiles_service
from app.services import study_history as study_service
from app.services.database import DatabaseError

log = logging.getLogger(__name__)

router = APIRouter(tags=["Profile"])


async def _safe_stats(user_id: str) -> dict:
    """Return user stats, returning zeros if the database is unavailable."""
    try:
        decks = await decks_service.list_decks(user_id)
        flashcards = sum(len(item.get("cards") or []) for item in decks)
    except DatabaseError as exc:
        log.warning("Could not load decks for stats: %s", exc)
        decks, flashcards = [], 0
    try:
        reviews = await study_service.list_reviews(user_id)
    except DatabaseError as exc:
        log.warning("Could not load reviews for stats: %s", exc)
        reviews = []
    return {
        "total_decks": len(decks),
        "total_flashcards": flashcards,
        "study_reviews": len(reviews),
    }


async def _merged_profile(user: dict) -> dict:
    profile = None
    try:
        profile = await profiles_service.get_profile(user["id"])
    except DatabaseError as exc:
        log.warning("Could not load profile from DB: %s", exc)
    base = {
        "id": user["id"],
        "name": user.get("name", "Learner"),
        "email": user.get("email", ""),
        "avatar_url": user.get("avatar_url"),
        "created_at": user.get("created_at", ""),
    }
    if profile:
        base["name"] = profile.get("name") or base["name"]
        base["avatar_url"] = profile.get("avatar_url") or base["avatar_url"]
        base["created_at"] = profile.get("created_at") or base["created_at"]
    base.update(await _safe_stats(user["id"]))
    return base


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user: dict = Depends(current_user)) -> ProfileResponse:
    return ProfileResponse(**await _merged_profile(user))


@router.put("/profile", response_model=ProfileResponse)
async def update_profile(payload: ProfileUpdate, user: dict = Depends(current_user)) -> ProfileResponse:
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        try:
            await profiles_service.upsert_profile(user["id"], updates)
        except DatabaseError as exc:
            log.error("Profile save failed for user %s: %s", user["id"], exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Profile could not be saved to the database. {exc}",
            )
    return ProfileResponse(**await _merged_profile(user))