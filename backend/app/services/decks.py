from datetime import datetime, timezone

from app.services.database import DatabaseService

decks = DatabaseService("decks")


def _humanized_updated(value: str) -> str:
    try:
        updated = datetime.fromisoformat(value.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        days = (now - updated).days
        if days <= 0:
            return "Today"
        if days == 1:
            return "Yesterday"
        return updated.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return value


async def list_decks(user_id: str) -> list[dict]:
    rows = await decks.list(filters={"user_id": user_id})
    for row in rows:
        row["updated"] = _humanized_updated(row.get("updated_at") or row.get("updated") or "")
    return rows


async def get_deck(user_id: str, deck_id: str | int) -> dict | None:
    rows = await decks.list(filters={"id": deck_id, "user_id": user_id}, limit=1)
    if not rows:
        return None
    row = rows[0]
    row["updated"] = _humanized_updated(row.get("updated_at") or "")
    return row


async def create_deck(user_id: str, payload: dict) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    row = {
        "user_id": user_id,
        "title": payload["title"],
        "description": payload.get("description", ""),
        "subject": payload.get("subject", "General"),
        "cards": payload.get("cards") or [],
        "progress": payload.get("progress", 0),
        "color": payload.get("color", "from-indigo-400 to-cyan-400"),
        "updated": "Just now",
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    created = await decks.create(row)
    created["updated"] = "Just now"
    return created


async def update_deck(user_id: str, deck_id: str | int, payload: dict) -> dict | None:
    existing = await get_deck(user_id, deck_id)
    if not existing:
        return None
    updates = {key: value for key, value in payload.items() if value is not None}
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    row = {"title", "description", "subject", "cards", "progress", "color"}
    updates = {key: value for key, value in updates.items() if key in row}
    updated = await decks.update(deck_id, updates)
    if updated is None:
        return None
    updated["updated"] = _humanized_updated(updated.get("updated_at") or "")
    return updated


async def delete_deck(user_id: str, deck_id: str | int) -> bool:
    existing = await get_deck(user_id, deck_id)
    if not existing:
        return False
    return await decks.delete(deck_id)


async def list_cards(user_id: str) -> list[dict]:
    """Flatten all cards across a user's decks with their deck reference."""
    rows = await list_decks(user_id)
    cards = []
    for deck in rows:
        for card in deck.get("cards") or []:
            cards.append({**card, "deck_id": deck["id"], "deck_title": deck.get("title", "")})
    return cards