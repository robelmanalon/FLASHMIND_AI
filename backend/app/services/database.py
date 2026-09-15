import asyncio
import logging
from typing import Any, Callable

from postgrest.exceptions import APIError

from app.services.supabase import get_admin_client, get_fallback_client

log = logging.getLogger(__name__)


class DatabaseError(RuntimeError):
    """Raised when a Supabase database operation fails."""


class DatabaseService:
    """Async facade over supabase-py's table API.

    Tries the service-role client first (bypasses RLS). If the key is
    invalid or missing, falls back to the anon client (RLS applies).
    """

    def __init__(self, table: str):
        self.table = table

    def _clients(self):
        clients = []
        for factory, label in ((get_admin_client, "admin"), (get_fallback_client, "fallback")):
            try:
                clients.append((factory(), label))
            except Exception as exc:
                log.warning("Supabase client '%s' unavailable: %s", label, exc)
        return clients

    def _attempt(self, build_query: Callable, *args: Any, **kwargs: Any):
        last_error: Exception | None = None
        for client, label in self._clients():
            try:
                query = build_query(client, *args, **kwargs)
                return query.execute().data
            except APIError as exc:
                last_error = exc
                log.warning("Supabase operation failed on '%s' client: %s", label, exc)
                continue
            except Exception as exc:
                last_error = exc
                log.warning("Supabase operation raised on '%s' client: %s", label, exc)
                continue
        raise DatabaseError(f"Supabase table operation unavailable: {last_error}") from last_error

    async def list(self, *, filters: dict[str, Any] | None = None, limit: int | None = None) -> list[dict]:
        def run() -> list[dict]:
            def build(client):
                query = client.table(self.table).select("*")
                for key, value in (filters or {}).items():
                    query = query.eq(key, value)
                if limit:
                    query = query.limit(limit)
                return query
            return self._attempt(build) or []
        return await asyncio.to_thread(run)

    async def get(self, record_id: str | int, *, id_column: str = "id") -> dict | None:
        rows = await self.list(filters={id_column: record_id}, limit=1)
        return rows[0] if rows else None

    async def create(self, payload: dict[str, Any]) -> dict:
        def run() -> list[dict]:
            def build(client):
                return client.table(self.table).insert(payload)
            return self._attempt(build)
        rows = await asyncio.to_thread(run)
        return rows[0] if rows else payload

    async def update(self, record_id: str | int, payload: dict[str, Any], *, id_column: str = "id") -> dict | None:
        def run() -> list[dict]:
            def build(client):
                return client.table(self.table).update(payload).eq(id_column, record_id)
            return self._attempt(build) or []
        rows = await asyncio.to_thread(run)
        return rows[0] if rows else None

    async def delete(self, record_id: str | int, *, id_column: str = "id") -> bool:
        def run() -> bool:
            def build(client):
                return client.table(self.table).delete().eq(id_column, record_id)
            return bool(self._attempt(build))
        return await asyncio.to_thread(run)