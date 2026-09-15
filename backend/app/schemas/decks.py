from pydantic import BaseModel, Field


class FlashcardCard(BaseModel):
    id: int
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    hint: str | None = None
    bookmarked: bool = False
    favorite: bool = False


class DeckCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    subject: str = Field(default="General", max_length=80)
    cards: list[FlashcardCard] = Field(default_factory=list)
    progress: int = Field(default=0, ge=0, le=100)
    color: str = Field(default="from-indigo-400 to-cyan-400", max_length=80)


class DeckUpdate(DeckCreate):
    pass


class DeckResponse(DeckCreate):
    id: str
    user_id: str
    updated: str
    created_at: str
    updated_at: str