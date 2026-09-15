from datetime import datetime, timedelta, timezone


def schedule_review(card: dict, rating: str) -> dict:
    """Apply a small SM-2-inspired schedule and return the updated card fields."""
    ease = float(card.get("ease_factor", 2.5))
    interval = int(card.get("interval", 1))
    repetitions = int(card.get("repetitions", 0))

    if rating == "again":
        ease = max(1.3, ease - 0.2)
        interval = 0
        repetitions = 0
        next_review = datetime.now(timezone.utc) + timedelta(minutes=10)
    elif rating == "hard":
        ease = max(1.3, ease - 0.15)
        interval = max(1, round(interval * 1.2))
        repetitions += 1
        next_review = datetime.now(timezone.utc) + timedelta(days=interval)
    elif rating == "good":
        interval = 1 if repetitions == 0 else 6 if repetitions == 1 else max(1, round(interval * ease))
        repetitions += 1
        next_review = datetime.now(timezone.utc) + timedelta(days=interval)
    else:
        ease += 0.15
        interval = 4 if repetitions == 0 else max(1, round(interval * ease * 1.3))
        repetitions += 1
        next_review = datetime.now(timezone.utc) + timedelta(days=interval)

    return {"ease_factor": round(ease, 2), "interval": interval, "repetitions": repetitions, "next_review_date": next_review.isoformat()}