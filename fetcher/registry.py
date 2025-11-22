from typing import Dict, List

from .base import BaseFetcher


class FetcherRegistry:
    _fetchers: Dict[str, BaseFetcher] = {}

    @classmethod
    def register(cls, fetcher: BaseFetcher):
        cls._fetchers[fetcher.source_id] = fetcher

    @classmethod
    def get(cls, source_id: str) -> BaseFetcher:
        if source_id not in cls._fetchers:
            raise ValueError(f"Source '{source_id}' not registered")
        return cls._fetchers[source_id]

    @classmethod
    def all(cls) -> Dict[str, BaseFetcher]:
        return cls._fetchers.copy()

    @classmethod
    def list_source_ids(cls) -> List[str]:
        return list(cls._fetchers.keys())
