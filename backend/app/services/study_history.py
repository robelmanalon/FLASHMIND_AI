from app.services.database import DatabaseService

study_history = DatabaseService("study_reviews")


async def create_review(payload: dict) -> dict:
    return await study_history.create(payload)


async def list_reviews(user_id: str, flashcard_id: int | str | None = None) -> list[dict]:
    filters = {"user_id": user_id}
    if flashcard_id is not None:
        filters["flashcard_id"] = flashcard_id
    return await study_history.list(filters=filters)