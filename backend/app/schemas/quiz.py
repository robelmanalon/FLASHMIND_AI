from typing import Literal

from pydantic import BaseModel, Field


class QuizGenerateRequest(BaseModel):
    deck_id: int | None = None
    question_count: int = Field(default=5, ge=1, le=20)
    types: list[Literal["multiple-choice", "true-false", "identification", "fill-blank"]] | None = None


class QuizQuestion(BaseModel):
    id: int
    type: str
    prompt: str
    options: list[str] | None = None


class QuizResponse(BaseModel):
    id: str
    deck_id: int | None
    question_count: int
    questions: list[QuizQuestion]
    created_at: str


class SavedQuizBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class SavedQuizRequest(SavedQuizBase):
    questions: list[dict] = Field(default_factory=list)


class SavedQuizResponse(SavedQuizBase):
    id: str
    user_id: str
    questions: list[dict] = Field(default_factory=list)
    question_count: int = 0
    created_at: str