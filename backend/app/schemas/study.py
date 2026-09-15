from pydantic import BaseModel, Field


class StudyReviewRequest(BaseModel):
    flashcard_id: int
    rating: str = Field(pattern="^(again|hard|good|easy)$")
    response_time_seconds: int | None = Field(default=None, ge=0)


class StudyReviewResponse(BaseModel):
    id: str
    flashcard_id: int
    rating: str
    response_time_seconds: int | None
    reviewed_at: str
    ease_factor: float
    interval: int
    repetitions: int
    next_review_date: str