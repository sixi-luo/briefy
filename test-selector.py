"""测试 select_top_news 函数"""

import logging
from datetime import datetime

from logger.logging import setup_logger
from summary.selector import select_top_news

setup_logger()


def test_select_top_news():
    """测试 select_top_news 函数"""
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"测试日期: {date}\n")

    # 测试基本功能
    print("测试1: 基本选择功能（top_n=10）")
    result = select_top_news(date, top_n=10)
    print(f"  结果: 选出 {len(result)} 条新闻")
    assert len(result) <= 10, f"应该最多返回10条，实际返回{len(result)}条"
    if result:
        print(f"  第一条: {result[0]['title'][:50]}...")
        print(f"  来源: {result[0]['source_name']}")
        print(f"  排名: {result[0]['rank']}")
        print(f"  分数: {result[0]['weighted_score']}")
    print("  ✅ 通过\n")

    # 测试去重功能（检查是否有相似标题）
    print("测试2: 检查去重功能")
    result = select_top_news(date, top_n=20)
    titles = [item["title"] for item in result]
    print(f"  结果: 选出 {len(result)} 条新闻")
    print(f"  标题数量: {len(titles)}")
    print(f"  唯一标题数量: {len(set(titles))}")
    assert len(titles) == len(set(titles)), "应该没有完全重复的标题"
    print("  ✅ 通过\n")

    print("所有测试通过！✅")


if __name__ == "__main__":
    test_select_top_news()
