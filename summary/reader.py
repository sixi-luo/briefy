"""Reader API 调用模块 - 获取文章内容"""

import logging
from typing import List, Optional

import httpx

from config import cfg

logger = logging.getLogger(__name__)

MAX_CONCURRENT = 5


async def fetch_content(url: str) -> Optional[str]:
    """
    从指定 URL 获取文章内容

    Args:
        url: 文章 URL

    Returns:
        Markdown 格式的文章内容，失败返回 None
    """
    if not cfg.reader_api_key:
        logger.error("READER_API_KEY not set")
        return None

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                cfg.reader_api_endpoint,
                headers={
                    "Authorization": f"Bearer {cfg.reader_api_key}",
                    "Content-Type": "application/json",
                },
                json={"url": url},
            )
        response.raise_for_status()
        data = response.json()

        # 检查返回码
        if data.get("code") != 0:
            logger.warning(f"Reader API 返回错误: {data.get('message')} (URL: {url})")
            return None

        # 提取 markdown 内容
        markdown_content = data.get("data", {}).get("markdown")
        if markdown_content:
            return markdown_content
        else:
            logger.warning(f"Reader API 返回数据中没有 markdown 字段 (URL: {url})")
            return None

    except httpx.TimeoutException:
        logger.warning(f"Reader API 调用超时: {url}")
        return None
    except httpx.HTTPStatusError as e:
        logger.warning(f"Reader API HTTP 错误 {e.response.status_code}: {url}")
        return None
    except Exception as e:
        logger.warning(f"Reader API 调用失败 {url}: {e}")
        return None


async def fetch_contents_batch(news_list: List[dict]) -> List[dict]:
    """
    批量获取新闻内容（并发控制）

    Args:
        news_list: 新闻列表，每个元素包含 title, url, source_name, rank 等字段

    Returns:
        带内容的新闻列表，每个元素添加了 markdown_content 字段
    """
    import asyncio

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def fetch_with_limit(news_item: dict) -> dict:
        async with semaphore:
            url = news_item["url"]
            logger.debug(f"获取内容: {news_item['title'][:50]}...")
            markdown_content = await fetch_content(url)
            news_item["markdown_content"] = markdown_content
            return news_item

    # 并发获取所有内容
    tasks = [fetch_with_limit(news_item.copy()) for news_item in news_list]
    results = await asyncio.gather(*tasks)

    # 统计成功数量
    success_count = sum(1 for item in results if item.get("markdown_content"))
    logger.info(f"成功获取 {success_count}/{len(results)} 篇文章内容")

    return list(results)
