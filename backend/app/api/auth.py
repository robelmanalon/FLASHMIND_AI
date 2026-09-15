from fastapi import APIRouter, HTTPException, status

from app.database.store import USERS, new_uuid, now_iso, password_hash
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from app.services.authentication import admin_create_user, sign_in, sign_up
from app.services.profiles import upsert_profile
from app.services.supabase import SupabaseConfigurationError
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _user_response(user: object, fallback_name: str = "Learner") -> UserResponse:
    def read(key: str, default=None):
        return user.get(key, default) if isinstance(user, dict) else getattr(user, key, default)

    metadata = read("user_metadata") or {}
    created_at = read("created_at") or now_iso()
    return UserResponse(
        id=str(read("id")),
        name=metadata.get("name", fallback_name),
        email=read("email"),
        avatar_url=metadata.get("avatar_url"),
        created_at=str(created_at),
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest) -> AuthResponse:
    if settings.supabase_url and settings.supabase_key:
        try:
            # Development mode uses the server-only Admin API so signup never sends SMTP email.
            if settings.supabase_auto_confirm_users and settings.supabase_service_role_key:
                result = await admin_create_user(payload.email, payload.password, {"name": payload.name})
                user = result.get("user") if isinstance(result, dict) else result
                session_result = await sign_in(payload.email, payload.password)
                session_user = session_result.get("user")
                session = session_result.get("session")
                if not session_user or not session:
                    raise HTTPException(status_code=502, detail="User was created, but Supabase did not return a session")
                try:
                    await upsert_profile(str(session_user.get("id")), {"name": payload.name, "avatar_url": None})
                except Exception:
                    pass
                return AuthResponse(access_token=session["access_token"], user=_user_response(session_user, payload.name))

            result = await sign_up(payload.email, payload.password, {"name": payload.name})
            user = result.get("user")
            session = result.get("session")
            if not user:
                raise HTTPException(status_code=502, detail="Supabase did not return a user")
            try:
                await upsert_profile(str(user.get("id")), {"name": payload.name, "avatar_url": None})
            except Exception:
                pass
            return AuthResponse(access_token=(session or {}).get("access_token", ""), user=_user_response(user, payload.name))
        except SupabaseConfigurationError:
            pass
        except Exception as error:
            message = str(error)
            if "invalid api key" in message.lower():
                raise HTTPException(status_code=503, detail="Supabase authentication is not configured. Replace SUPABASE_KEY in backend/.env with the current anon/publishable key from Supabase Project Settings > API, then restart FastAPI.") from error
            if "already registered" in message.lower() or "already exists" in message.lower():
                raise HTTPException(status_code=409, detail="An account with this email already exists") from error
            if "rate limit" in message.lower() or "too many" in message.lower():
                if settings.supabase_auto_confirm_users and not settings.supabase_service_role_key:
                    raise HTTPException(status_code=503, detail="Auto-confirm is enabled, but SUPABASE_SERVICE_ROLE_KEY is missing. Add a new server-only service-role key to backend/.env, then restart FastAPI.") from error
                if settings.supabase_auto_confirm_users and settings.supabase_service_role_key:
                    try:
                        await admin_create_user(payload.email, payload.password, {"name": payload.name})
                        result = await sign_in(payload.email, payload.password)
                        user = result.get("user")
                        session = result.get("session")
                        if user and session:
                            return AuthResponse(access_token=session["access_token"], user=_user_response(user, payload.name))
                    except Exception as admin_error:
                        raise HTTPException(status_code=502, detail="Auto-confirm registration failed. Check SUPABASE_SERVICE_ROLE_KEY.") from admin_error
                raise HTTPException(status_code=429, detail="Supabase email rate limit exceeded. Wait before trying again or configure a custom SMTP provider in Supabase.") from error
            if "invalid" in message.lower() or "email" in message.lower() or "password" in message.lower():
                raise HTTPException(status_code=422, detail=message) from error
            raise HTTPException(status_code=502, detail="Supabase registration failed. Check the backend Supabase configuration.") from error

    if any(user["email"].lower() == payload.email.lower() for user in USERS):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = {"id": new_uuid(), "name": payload.name, "email": payload.email, "password_hash": password_hash(payload.password), "avatar_url": None, "created_at": now_iso()}
    USERS.append(user)
    return AuthResponse(access_token=user["id"], user=UserResponse(**user))


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest) -> AuthResponse:
    if settings.supabase_url and settings.supabase_key:
        try:
            result = await sign_in(payload.email, payload.password)
            user = result.get("user")
            session = result.get("session")
            if not user or not session:
                raise HTTPException(status_code=401, detail="Email confirmation may be required before signing in")
            return AuthResponse(access_token=session["access_token"], user=_user_response(user))
        except SupabaseConfigurationError:
            pass
        except HTTPException:
            raise
        except Exception as error:
            if "invalid api key" in str(error).lower():
                raise HTTPException(status_code=503, detail="Supabase authentication is not configured. Replace SUPABASE_KEY in backend/.env with the current anon/publishable key from Supabase Project Settings > API, then restart FastAPI.") from error
            raise HTTPException(status_code=401, detail="Invalid email or password") from error

    user = next((item for item in USERS if item["email"].lower() == payload.email.lower()), None)
    if not user or user["password_hash"] != password_hash(payload.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return AuthResponse(access_token=user["id"], user=UserResponse(**user))