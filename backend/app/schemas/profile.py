from pydantic import BaseModel, EmailStr, Field


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    avatar_url: str | None = None


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    avatar_url: str | None = None
    created_at: str
    total_decks: int
    total_flashcards: int
    study_reviews: int