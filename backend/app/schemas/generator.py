from typing import Literal

from pydantic import BaseModel, Field


QuestionType = Literal["multiple-choice", "true-false", "identification"]


class GeneratedFlashcard(BaseModel):
    question: str
    answer: str
    explanation: str


class GeneratedQuizQuestion(BaseModel):
    type: QuestionType
    question: str
    answer: str
    options: list[str]
    explanation: str


class GeneratedContent(BaseModel):
    flashcards: list[GeneratedFlashcard]
    quiz_questions: list[GeneratedQuizQuestion]


class GeneratorResponse(BaseModel):
    filename: str
    content_type: str
    characters_extracted: int
    chunks_processed: int
    result: GeneratedContent