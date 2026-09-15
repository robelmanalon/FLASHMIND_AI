from fastapi import Header, HTTPException, status

from app.config import settings
from app.services.supabase import get_supabase_client


def current_user(authorization: str | None = Header(default=None)) -> dict:
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        if settings.supabase_url and settings.supabase_key:
            try:
                user = get_supabase_client().auth.get_user(token).user
                return {"id": str(user.id), "name": (user.user_metadata or {}).get("name", "Learner"), "email": user.email, "avatar_url": (user.user_metadata or {}).get("avatar_url"), "created_at": str(user.created_at)}
            except Exception as error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token") from error
        return {"id": token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")