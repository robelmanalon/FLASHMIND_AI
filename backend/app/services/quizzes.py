from app.services.database import DatabaseService

quizzes = DatabaseService("saved_quizzes")


async def create_quiz(user_id: str, payload: dict) -> dict:
    return await quizzes.create({"user_id": user_id, "title": payload.get("title", "Untitled quiz"), "questions": payload.get("questions") or []})


async def list_quizzes(user_id: str) -> list[dict]:
    return await quizzes.list(filters={"user_id": user_id})


async def get_quiz(user_id: str, quiz_id: str | int) -> dict | None:
    rows = await quizzes.list(filters={"id": quiz_id, "user_id": user_id}, limit=1)
    return rows[0] if rows else None


async def delete_quiz(user_id: str, quiz_id: str | int) -> bool:
    existing = await get_quiz(user_id, quiz_id)
    if not existing:
        return False
    return await quizzes.delete(quiz_id)