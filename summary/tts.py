"""TTS 文本转语音功能"""

import logging
from pathlib import Path

import edge_tts

logger = logging.getLogger(__name__)

# 默认语音选择（中文女声）
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


async def generate_audio(text: str, output_path: Path, voice: str = DEFAULT_VOICE) -> Path:
    """
    生成音频文件

    Args:
        text: 要转换的文本
        output_path: 输出文件路径
        voice: 语音选择，默认使用中文女声

    Returns:
        生成的音频文件路径
    """
    try:
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 使用 edge-tts 生成音频
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))

        logger.info(f"音频已生成: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"生成音频失败: {e}")
        raise
