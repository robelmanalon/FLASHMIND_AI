from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import current_user
from app.schemas.study import StudyReviewRequest, StudyReviewResponse
from app.services import decks as decks_service
from app.services import study_history as study_service
from app.services.spaced_repetition import schedule_review

router = APIRouter(prefix="/study", tags=["Study History"])


@router.post("/review", response_model=StudyReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(payload: StudyReviewRequest, user: dict = Depends(current_user)) -> StudyReviewResponse:
    reviews = await study_service.list_reviews(user["id"], payload.flashcard_id)
    card = None
    deck_id = None
    deck_title = None
    if reviews:
        latest = max(reviews, key=lambda item: item.get("reviewed_at") or "")
        card = {
            "ease_factor": latest.get("ease_factor", 2.5),
            "interval": latest.get("interval", 1),
            "repetitions": latest.get("repetitions", 0),
        }
        card["deck_id"] = latest.get("deck_id")
    if not card:
        all_cards = await decks_service.list_cards(user["id"])
        for item in all_cards:
            if str(item.get("id")) == str(payload.flashcard_id):
                card = item
                deck_id = item.get("deck_id")
                deck_title = item.get("deck_title")
                break
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    schedule = schedule_review(card, payload.rating)
    review = {
        "user_id": user["id"],
        "deck_id": card.get("deck_id") or deck_id,
        "flashcard_id": payload.flashcard_id,
        "rating": payload.rating,
        "response_time_seconds": payload.response_time_seconds,
        "ease_factor": schedule["ease_factor"],
        "interval": schedule["interval"],
        "repetitions": schedule["repetitions"],
        "next_review_date": schedule["next_review_date"],
    }
    created = await study_service.create_review(review)
    created["deck_title"] = deck_title
    return StudyReviewResponse(**created)