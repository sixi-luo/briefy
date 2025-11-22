"""测试汇总功能"""

import logging
from datetime import datetime

from logger.logging import setup_logger
from storage.aggregator import DailyAggregator

setup_logger()
logger = logging.getLogger(__name__)


def main():
    """测试生成汇总文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"开始生成 {today} 的汇总文件...")
    generator = DailyAggregator()
    generator.generate(today)


if __name__ == "__main__":
    main()
