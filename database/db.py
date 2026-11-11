"""In-memory database support for the application."""

from __future__ import annotations

from typing import Any, Dict, List


class Database:
    """Simple in-memory persistence layer for mock data."""

    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def set(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        self._store.setdefault(collection, []).append(item)
        return item

    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        return list(self._store.get(collection, []))
