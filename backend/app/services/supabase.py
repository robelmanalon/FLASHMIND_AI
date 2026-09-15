from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


class SupabaseConfigurationError(RuntimeError):
    """Raised when a Supabase operation is requested without credentials."""


@lru_cache(maxsize=1)
def get_supabase_client(use_service_role: bool = False) -> Client:
    key = settings.supabase_service_role_key if use_service_role else settings.supabase_key
    if not settings.supabase_url or not key:
        raise SupabaseConfigurationError("SUPABASE_URL and SUPABASE_KEY are required")
    return create_client(settings.supabase_url, key)


def get_admin_client() -> Client:
    if not settings.supabase_service_role_key:
        raise SupabaseConfigurationError("SUPABASE_SERVICE_ROLE_KEY is required for admin operations")
    return get_supabase_client(use_service_role=True)