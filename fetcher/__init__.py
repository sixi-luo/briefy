from .baidu import BaiduFetcher
from .cailian import CailianFetcher
from .ifeng import IfengFetcher
from .jin10 import Jin10Fetcher
from .toutiao import ToutiaoFetcher
from .wallstreetcn import WallstreetcnFetcher
from .registry import FetcherRegistry

FetcherRegistry.register(BaiduFetcher())
FetcherRegistry.register(ToutiaoFetcher())
FetcherRegistry.register(IfengFetcher())
FetcherRegistry.register(CailianFetcher())
FetcherRegistry.register(WallstreetcnFetcher())
FetcherRegistry.register(Jin10Fetcher())

__all__ = [
    "BaiduFetcher",
    "ToutiaoFetcher",
    "IfengFetcher",
    "CailianFetcher",
    "WallstreetcnFetcher",
    "Jin10Fetcher",
    "FetcherRegistry",
]

