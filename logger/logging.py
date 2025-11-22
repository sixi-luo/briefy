import logging
import sys

DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

_configured = False


def setup_logger(level=logging.INFO, format_string=DEFAULT_FORMAT, force=False):
    global _configured
    if _configured and not force:
        return

    logging.basicConfig(
        level=level,
        format=format_string,
        stream=sys.stdout,
        force=force,
    )

    # 设置第三方库的日志级别
    logging.getLogger("httpx").setLevel(logging.WARNING)

    _configured = True
