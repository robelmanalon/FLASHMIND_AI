from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from uuid import uuid4


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def password_hash(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


USERS: list[dict] = [
    {
        "id": "user-demo",
        "name": "Alex Lee",
        "email": "alex@example.com",
        "password_hash": password_hash("password123"),
        "avatar_url": None,
        "created_at": now_iso(),
    }
]

DECKS: list[dict] = [
    {"id": 1, "user_id": "user-demo", "title": "Biology: Cell Structure", "description": "Core cell biology concepts.", "subject": "Biology", "created_at": now_iso(), "updated_at": now_iso()},
    {"id": 2, "user_id": "user-demo", "title": "Spanish essentials", "description": "Everyday vocabulary and phrases.", "subject": "Languages", "created_at": now_iso(), "updated_at": now_iso()},
]

FLASHCARDS: list[dict] = [
    {"id": 101, "deck_id": 1, "user_id": "user-demo", "question": "What is the powerhouse of the cell?", "answer": "The mitochondrion.", "hint": None, "ease_factor": 2.5, "interval": 1, "repetitions": 0, "next_review_date": now_iso(), "created_at": now_iso(), "updated_at": now_iso()},
    {"id": 102, "deck_id": 1, "user_id": "user-demo", "question": "What does the cell membrane do?", "answer": "It regulates what enters and leaves the cell.", "hint": None, "ease_factor": 2.5, "interval": 1, "repetitions": 0, "next_review_date": now_iso(), "created_at": now_iso(), "updated_at": now_iso()},
    {"id": 201, "deck_id": 2, "user_id": "user-demo", "question": "How do you say good morning?", "answer": "Buenos días.", "hint": None, "ease_factor": 2.5, "interval": 1, "repetitions": 0, "next_review_date": now_iso(), "created_at": now_iso(), "updated_at": now_iso()},
]

QUIZZES: dict[str, dict] = {}
STUDY_REVIEWS: list[dict] = []


def next_id(items: list[dict]) -> int:
    return max((int(item["id"]) for item in items), default=0) + 1


def new_uuid() -> str:
    return str(uuid4())