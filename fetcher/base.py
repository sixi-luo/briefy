from abc import ABC, abstractmethod
from typing import List

from .models import Trend


class BaseFetcher(ABC):
    @property
    @abstractmethod
    def source_id(self) -> str:
        pass

    @abstractmethod
    async def fetch(self) -> List[Trend]:
        """
        Fetch trending topics
        Returns: List[Trend] - List of trending topics
        """
        pass
