from app.services.database import DatabaseService

profiles = DatabaseService("profiles")


async def get_profile(user_id: str) -> dict | None:
    return await profiles.get(user_id)


async def upsert_profile(user_id: str, payload: dict) -> dict:
    existing = await profiles.get(user_id)
    if existing:
        return await profiles.update(user_id, payload)
    row = {"id": user_id, "name": payload.get("name", "Learner"), "avatar_url": payload.get("avatar_url")}
    return await profiles.create(row)


async def update_profile(user_id: str, payload: dict) -> dict | None:
    return await profiles.update(user_id, payload)