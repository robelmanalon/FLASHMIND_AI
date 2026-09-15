import asyncio
from typing import Any

from app.services.supabase import get_admin_client


class DatabaseService:
    """Async facade over supabase-py's table API using the service-role client.

    RLS is enabled on all tables, so the admin client is required for table
    operations. Ownership is enforced by the API layer via user_id filters.
    """

    def __init__(self, table: str):
        self.table = table

    def _query(self, operation: str, *args: Any, **kwargs: Any) -> Any:
        query = getattr(get_admin_client().table(self.table), operation)(*args, **kwargs)
        return query.execute().data

    async def list(self, *, filters: dict[str, Any] | None = None, limit: int | None = None) -> list[dict]:
        def run() -> list[dict]:
            query = get_admin_client().table(self.table).select("*")
            for key, value in (filters or {}).items():
                query = query.eq(key, value)
            if limit:
                query = query.limit(limit)
            return query.execute().data or []
        return await asyncio.to_thread(run)

    async def get(self, record_id: str | int, *, id_column: str = "id") -> dict | None:
        rows = await self.list(filters={id_column: record_id}, limit=1)
        return rows[0] if rows else None

    async def create(self, payload: dict[str, Any]) -> dict:
        rows = await asyncio.to_thread(self._query, "insert", payload)
        return rows[0] if rows else payload

    async def update(self, record_id: str | int, payload: dict[str, Any], *, id_column: str = "id") -> dict | None:
        def run() -> list[dict]:
            return get_admin_client().table(self.table).update(payload).eq(id_column, record_id).execute().data or []
        rows = await asyncio.to_thread(run)
        return rows[0] if rows else None

    async def delete(self, record_id: str | int, *, id_column: str = "id") -> bool:
        def run() -> bool:
            response = get_admin_client().table(self.table).delete().eq(id_column, record_id).execute()
            return bool(response.data)
        return await asyncio.to_thread(run)