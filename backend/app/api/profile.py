from fastapi import APIRouter, Depends

from app.api.dependencies import current_user
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services import decks as decks_service
from app.services import profiles as profiles_service
from app.services import study_history as study_service

router = APIRouter(tags=["Profile"])


async def _user_stats(user_id: str) -> dict:
    decks = await decks_service.list_decks(user_id)
    flashcards = sum(len(item.get("cards") or []) for item in decks)
    reviews = await study_service.list_reviews(user_id)
    return {
        "total_decks": len(decks),
        "total_flashcards": flashcards,
        "study_reviews": len(reviews),
    }


async def _merged_profile(user: dict) -> dict:
    profile = await profiles_service.get_profile(user["id"])
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
    base.update(await _user_stats(user["id"]))
    return base


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user: dict = Depends(current_user)) -> ProfileResponse:
    return ProfileResponse(**await _merged_profile(user))


@router.put("/profile", response_model=ProfileResponse)
async def update_profile(payload: ProfileUpdate, user: dict = Depends(current_user)) -> ProfileResponse:
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        await profiles_service.upsert_profile(user["id"], updates)
    return ProfileResponse(**await _merged_profile(user))