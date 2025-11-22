"""测试摘要生成完整流程"""

import asyncio
import logging
import time
from datetime import datetime

from logger.logging import setup_logger
from summary.generator import generate_daily_summary

setup_logger()
logger = logging.getLogger(__name__)


async def main():
    top_n = 3
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"测试日期: {date}\n")

    start_time = time.time()
    result = await generate_daily_summary(date, top_n=top_n)
    total_time = time.time() - start_time

    if result["success"]:
        print("\n✅ 摘要生成成功！")
        print(f"   输出文件: {result['output_file']}")
        print(f"   新闻数: {result['total_news']}")
        print(f"   获取内容: {result['content_fetched']}")
        print(f"   生成摘要: {result['summaries_generated']}")
        print(f"   总内容长度: {result['total_content_length']} 字符")
        print(f"   总耗时: {total_time:.2f}秒")
    else:
        print(f"\n❌ 摘要生成失败: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
