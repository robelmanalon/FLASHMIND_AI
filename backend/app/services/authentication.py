import asyncio

from app.services.supabase import get_admin_client, get_supabase_client


async def sign_up(email: str, password: str, metadata: dict | None = None) -> dict:
    return await asyncio.to_thread(lambda: get_supabase_client().auth.sign_up({"email": email, "password": password, "options": {"data": metadata or {}}}).model_dump())


async def sign_in(email: str, password: str) -> dict:
    return await asyncio.to_thread(lambda: get_supabase_client().auth.sign_in_with_password({"email": email, "password": password}).model_dump())


async def admin_create_user(email: str, password: str, metadata: dict | None = None) -> dict:
    def create() -> dict:
        response = get_admin_client().auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": metadata or {},
        })
        return response.model_dump() if hasattr(response, "model_dump") else response

    return await asyncio.to_thread(create)


async def sign_out(access_token: str) -> None:
    await asyncio.to_thread(lambda: get_supabase_client().auth.admin.sign_out(access_token))