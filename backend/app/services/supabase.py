import logging
from functools import lru_cache

from supabase import Client, create_client

from app.config import settings

log = logging.getLogger(__name__)


class SupabaseConfigurationError(RuntimeError):
    """Raised when a Supabase operation is requested without credentials."""


@lru_cache(maxsize=2)
def get_supabase_client(use_service_role: bool = False) -> Client:
    key = settings.supabase_service_role_key if use_service_role else settings.supabase_key
    if not settings.supabase_url or not key:
        raise SupabaseConfigurationError("SUPABASE_URL and SUPABASE_KEY are required")
    return create_client(settings.supabase_url, key)


def get_admin_client() -> Client:
    """Return the service-role client for privileged DB operations.

    If the service-role key is missing, fall back to the anon client so
    the application still works (RLS policies will apply).
    """
    if settings.supabase_service_role_key:
        return get_supabase_client(use_service_role=True)
    if settings.supabase_url and settings.supabase_key:
        log.warning(
            "SUPABASE_SERVICE_ROLE_KEY is not set — falling back to anon key. "
            "RLS policies will apply. Add the key to backend/.env for full access."
        )
        return get_supabase_client(use_service_role=False)
    raise SupabaseConfigurationError(
        "SUPABASE_URL and SUPABASE_KEY are required for database operations"
    )


def get_fallback_client() -> Client:
    """Return the anon client for read/write when admin client fails."""
    if not settings.supabase_url or not settings.supabase_key:
        raise SupabaseConfigurationError("SUPABASE_URL and SUPABASE_KEY are required")
    return get_supabase_client(use_service_role=False)