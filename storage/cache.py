import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, List

from fetcher.models import Trend


@dataclass
class CacheData:
    """缓存文件数据结构"""

    source: str
    """源ID"""

    timestamp: str
    """时间戳，格式：2025-11-22 17:50:00"""

    items: List[Trend]
    """热门内容列表"""


def omit_empty(data: Any) -> Any:
    """递归移除字典中的 None 值，实现类似 Go 的 omitempty 效果"""
    if isinstance(data, dict):
        return {k: omit_empty(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [omit_empty(item) for item in data]
    else:
        return data


class CacheStorage:
    """缓存存储（保存到 temp 目录）"""

    def __init__(self, base_path: Path | None = None):
        from config import cfg

        self.base_path = base_path or cfg.temp_dir

    def save(self, source_id: str, items: List[Trend]):
        """保存缓存文件"""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        filename = now.strftime("%Y%m%d_%H%M") + ".json"
        file_path = self.base_path / source_id / filename

        cache_data = CacheData(
            source=source_id,
            timestamp=timestamp,
            items=items,
        )

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            # json.dump(asdict(cache_data), f, ensure_ascii=False, indent=2)
            data_dict = omit_empty(asdict(cache_data))
            json.dump(data_dict, f, ensure_ascii=False, indent=2)
