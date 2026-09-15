from datetime import datetime, timezone

from app.services import decks as decks_service
from app.services import quizzes as quizzes_service
from app.services import study_history as study_service


async def build_dashboard(user_id: str) -> dict:
    decks = await decks_service.list_decks(user_id)
    cards = [card for deck in decks for card in (deck.get("cards") or [])]
    quizzes = await quizzes_service.list_quizzes(user_id)
    reviews = await study_service.list_reviews(user_id)
    today = datetime.now(timezone.utc).date().isoformat()

    weekly = {"labels": [], "values": []}
    from datetime import timedelta
    days = [(datetime.now(timezone.utc) - timedelta(days=offset)).date() for offset in range(6, -1, -1)]
    day_counts = {}
    for review in reviews:
        reviewed = (review.get("reviewed_at") or "")[:10]
        day_counts[reviewed] = day_counts.get(reviewed, 0) + 1
    for day in days:
        weekly["labels"].append(day.strftime("%a"))
        weekly["values"].append(day_counts.get(day.isoformat(), 0))

    correct = sum(1 for review in reviews if review.get("rating") in {"good", "easy"})
    accuracy = round((correct / len(reviews)) * 100, 1) if reviews else 0

    today_reviews = sum(1 for review in reviews if (review.get("reviewed_at") or "")[:10] == today)
    streak = _current_streak(reviews)

    recent_activity = []
    recent = sorted(reviews, key=lambda item: item.get("reviewed_at") or "", reverse=True)[:5]
    for review in recent:
        deck = next((d for d in decks if str(d.get("id")) == str(review.get("deck_id"))), None)
        deck_title = "{title}".format(title=(deck or {}).get("title", "a deck"))
        recent_activity.append({
            "id": review.get("id"),
            "title": "Reviewed a flashcard",
            "detail": deck_title,
            "time": _relative_time(review.get("reviewed_at")),
            "icon": "✓",
            "tone": "cyan",
        })

    for quiz in sorted(quizzes, key=lambda item: item.get("created_at") or "", reverse=True)[:5]:
        recent_activity.append({
            "id": quiz.get("id"),
            "title": "Saved a quiz",
            "detail": quiz.get("title", "Quiz"),
            "time": _relative_time(quiz.get("created_at")),
            "icon": "✓",
            "tone": "purple",
        })

    recent_decks = [{
        "id": deck.get("id"),
        "title": deck.get("title", "Untitled deck"),
        "cards": len(deck.get("cards") or []),
        "progress": deck.get("progress", 0),
        "color": _color(deck.get("subject")),
        "lastStudied": deck.get("updated", ""),
    } for deck in sorted(decks, key=lambda item: item.get("updated_at") or "", reverse=True)[:3]]

    continue_studying = None
    if decks:
        first = decks[0]
        continue_studying = {
            "title": first.get("title", ""),
            "subtitle": first.get("description", ""),
            "remaining": len(first.get("cards") or []),
            "total": len(first.get("cards") or []),
            "progress": int(first.get("progress") or 0),
        }

    return {
        "stats": [
            {"label": "Total decks", "value": str(len(decks)), "detail": f"{len(quizzes)} saved quizzes", "icon": "▦", "tone": "indigo"},
            {"label": "Total flashcards", "value": str(len(cards)), "detail": f"{today_reviews} reviewed today", "icon": "▤", "tone": "cyan"},
            {"label": "Quiz accuracy", "value": f"{accuracy}%", "detail": "good + easy ratings", "icon": "✓", "tone": "purple"},
            {"label": "Study streak", "value": f"{streak} days", "detail": "Reviews per day", "icon": "↗", "tone": "cyan"},
        ],
        "recentDecks": recent_decks,
        "continueStudying": continue_studying or {"title": "Explore a deck", "subtitle": "Create or generate your first deck", "remaining": 0, "total": 0, "progress": 0},
        "todayProgress": {"completed": today_reviews, "goal": 20, "minutes": min(60, today_reviews * 3), "sessions": max(0, today_reviews // 5)},
        "weeklyStudy": weekly,
        "activity": recent_activity,
    }


async def build_progress(user_id: str) -> dict:
    decks = await decks_service.list_decks(user_id)
    reviews = await study_service.list_reviews(user_id)
    today = datetime.now(timezone.utc).date().isoformat()

    day_counts = {}
    for review in reviews:
        reviewed = (review.get("reviewed_at") or "")[:10]
        day_counts[reviewed] = day_counts.get(reviewed, 0) + 1

    streak = _current_streak(reviews)
    best = streak
    running = 0
    for date_key in sorted(day_counts):
        if day_counts[date_key] > 0:
            running += 1
            best = max(best, running)
        else:
            running = 0

    reviewed_today = day_counts.get(today, 0)
    accuracy_values = []
    for day in _last_seven_days():
        reviews_that_day = [r for r in reviews if (r.get("reviewed_at") or "")[:10] == day.isoformat()]
        correct = sum(1 for r in reviews_that_day if r.get("rating") in {"good", "easy"})
        accuracy_values.append(round((correct / len(reviews_that_day)) * 100) if reviews_that_day else 0)

    upcoming = []
    for deck in decks:
        for card in (deck.get("cards") or [])[:2]:
            upcoming.append({
                "id": card.get("id"),
                "deck": deck.get("title", ""),
                "card": card.get("question", ""),
                "due": "Today",
                "interval": f"{int(deck.get('cards', []).index(card) % 6 + 1)} days",
                "tone": "cyan",
            })
            if len(upcoming) >= 4:
                break
        if len(upcoming) >= 4:
            break

    return {
        "streak": streak,
        "bestStreak": best,
        "reviewedToday": reviewed_today,
        "dailyGoal": 20,
        "accuracy": {"labels": [day.strftime("%a") for day in _last_seven_days()], "values": accuracy_values},
        "heatmap": [min(5, day_counts.get(day.isoformat(), 0)) for day in _last_weeks(8)],
        "upcoming": upcoming,
    }


def _last_seven_days():
    from datetime import timedelta
    return [(datetime.now(timezone.utc) - timedelta(days=offset)).date() for offset in range(6, -1, -1)]


def _last_weeks(weeks: int):
    from datetime import timedelta
    return [(datetime.now(timezone.utc) - timedelta(days=day)).date() for day in range(weeks * 7 - 1, -1, -1)]


def _current_streak(reviews: list[dict]) -> int:
    from datetime import timedelta
    dates = {r.get("reviewed_at", "")[:10] for r in reviews if r.get("reviewed_at")}
    if not dates:
        return 0
    streak = 0
    day = datetime.now(timezone.utc).date()
    if day.isoformat() not in dates:
        day -= timedelta(days=1)
    while day.isoformat() in dates:
        streak += 1
        day -= timedelta(days=1)
    return streak


def _relative_time(value: str | None) -> str:
    if not value:
        return "Recently"
    try:
        when = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - when
        if delta.days <= 0:
            return "Today"
        if delta.days == 1:
            return "Yesterday"
        return f"{delta.days} days ago"
    except (ValueError, TypeError):
        return "Recently"


def _color(subject: str | None) -> str:
    subject = (subject or "").lower()
    if "spani" in subject or "language" in subject:
        return "gold"
    if "design" in subject:
        return "coral"
    return "mint"