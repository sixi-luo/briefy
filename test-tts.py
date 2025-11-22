import asyncio
import json
import time

import edge_tts

from config import cfg
from summary.generator import format_text
from summary.tts import generate_audio


async def test_tts():
    # 读取已生成的摘要数据
    json_file = cfg.summaries_dir / "2025-11-22.json"

    if not json_file.exists():
        print(f"❌ 文件不存在: {json_file}")
        print("请先运行 test-generator.py 生成摘要数据")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"日期: {data['date']}，共 {data['total_news']} 条新闻\n")
    print("=" * 60)

    # 生成文本
    print("\n📝 生成 TTS 文本:")
    print("-" * 60)
    text_start = time.time()
    text = format_text(data)
    text_time = time.time() - text_start
    print(f"文本长度: {len(text)} 字符，生成耗时: {text_time:.2f} 秒\n")
    print(text)

    # 生成音频
    print("\n🎙️  生成音频:")
    print("-" * 60)
    cfg.audio_dir.mkdir(parents=True, exist_ok=True)
    audio_file = cfg.audio_dir / f"{data['date']}.mp3"

    try:
        audio_start = time.time()
        await generate_audio(text, audio_file)
        audio_time = time.time() - audio_start
        file_size = audio_file.stat().st_size / 1024
        print(f"✅ 音频已生成: {audio_file}")
        print(f"文件大小: {file_size:.2f} KB，生成耗时: {audio_time:.2f} 秒，平均速度: {len(text) / audio_time:.0f} 字符/秒")
    except Exception as e:
        print(f"❌ 生成音频失败: {e}")
        return


async def test_list_voices():
    """列出所有语音"""
    voices = await edge_tts.list_voices()
    print(f"共找到 {len(voices)} 个语音\n")

    # 按语言分组统计
    locales = {}
    for voice in voices:
        locale = voice.get("Locale", "Unknown")
        locales[locale] = locales.get(locale, 0) + 1

    print("各语言语音数量统计（前20个）:")
    for locale, count in sorted(locales.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {locale}: {count}")


async def test_chinese_voices():
    """获取中文语音列表"""
    voices = await edge_tts.list_voices()
    chinese_voices = [v for v in voices if v["Locale"].startswith("zh-CN")]
    print(f"共找到 {len(chinese_voices)} 个中文语音\n")

    for voice in chinese_voices:
        short_name = voice.get("ShortName", "Unknown")
        local_name = voice.get("LocalName", "Unknown")
        gender = voice.get("Gender", "Unknown")
        print(f"  {local_name} ({short_name}, {gender})")


if __name__ == "__main__":
    # asyncio.run(test_tts())
    # asyncio.run(test_list_voices())
    asyncio.run(test_chinese_voices())
