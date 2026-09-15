from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import current_user
from app.schemas.quiz import SavedQuizRequest, SavedQuizResponse
from app.services import quizzes as quizzes_service

router = APIRouter(prefix="/quiz", tags=["Quizzes", "AI Generation"])


def _with_created_at(quiz: dict) -> dict:
    quiz["createdAt"] = _short_date(quiz.get("created_at"))
    quiz["question_count"] = len(quiz.get("questions") or [])
    return quiz


def _short_date(value: str | None) -> str:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date().isoformat()
    except (ValueError, TypeError):
        return value or ""


@router.get("/saved", response_model=list[SavedQuizResponse])
async def list_saved_quizzes(user: dict = Depends(current_user)) -> list[SavedQuizResponse]:
    quizzes = await quizzes_service.list_quizzes(user["id"])
    return [SavedQuizResponse(**_with_created_at(quiz)) for quiz in quizzes]


@router.post("/saved", response_model=SavedQuizResponse, status_code=status.HTTP_201_CREATED)
async def create_saved_quiz(payload: SavedQuizRequest, user: dict = Depends(current_user)) -> SavedQuizResponse:
    quiz = await quizzes_service.create_quiz(user["id"], payload.model_dump())
    return SavedQuizResponse(**_with_created_at(quiz))


@router.get("/saved/{quiz_id}", response_model=SavedQuizResponse)
async def get_saved_quiz(quiz_id: str, user: dict = Depends(current_user)) -> SavedQuizResponse:
    quiz = await quizzes_service.get_quiz(user["id"], quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return SavedQuizResponse(**_with_created_at(quiz))


@router.delete("/saved/{quiz_id}", response_model=dict[str, str])
async def delete_saved_quiz(quiz_id: str, user: dict = Depends(current_user)) -> dict[str, str]:
    removed = await quizzes_service.delete_quiz(user["id"], quiz_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"message": "Quiz deleted", "id": quiz_id}


@router.get("/saved/{quiz_id}/start", response_model=SavedQuizResponse)
async def start_saved_quiz(quiz_id: str, user: dict = Depends(current_user)) -> SavedQuizResponse:
    quiz = await quizzes_service.get_quiz(user["id"], quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return SavedQuizResponse(**_with_created_at(quiz))