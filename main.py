from fastapi import BackgroundTasks
import asyncio
import json
import logging
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from config import cfg
from logger.logging import setup_logger
from scheduler import scheduled_task
from web.render import render_page

setup_logger()
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理——完全非阻塞启动"""
    logger.info("Initializing scheduler in background...")
    
    # 在后台启动调度器和初始任务，不阻塞 lifespan
    asyncio.create_task(start_scheduler_and_initial_task())
    
    yield  # 立即让出控制权，服务器开始接收请求
    
    logger.info("Stopping scheduler...")
    scheduler.shutdown()

async def start_scheduler_and_initial_task():
    """将调度器启动和首次抓取放到后台执行"""
    # 给服务器一点时间完全启动（非必须，但安全）
    await asyncio.sleep(0.5)
    
    # 添加定时任务
    scheduler.add_job(
        scheduled_task,
        "interval",
        minutes=30,
        id="fetch_and_aggregate",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started: fetch and aggregate every 30 minutes")
    
    # 执行首次抓取（不等待完成，直接创建任务）
    asyncio.create_task(scheduled_task())
    logger.info("Initial fetch task created")

app = FastAPI(title="Briefy - AI 驱动的每日简报", lifespan=lifespan)

# ---------- 首页：正常返回渲染的 HTML 页面 ----------
@app.get("/", response_class=HTMLResponse)
async def index(date: str | None = Query(None, description="日期，格式：YYYY-MM-DD")):
    """首页，展示指定日期的热搜数据"""
    try:
        html_content = render_page(date)
        return HTMLResponse(content=html_content)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

# ---------- API 接口 ----------
@app.get("/api/summary/{date}")
async def get_summary(date: str):
    """获取指定日期的摘要数据"""
    summary_file = cfg.summaries_dir / f"{date}.json"
    if not summary_file.exists():
        raise HTTPException(status_code=404, detail=f"未找到 {date} 的摘要数据")
    try:
        with open(summary_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取摘要数据失败: {str(e)}")

@app.get("/api/audio/{date}")
async def get_audio(date: str):
    """获取指定日期的音频"""
    audio_file = cfg.audio_dir / f"{date}.mp3"
    if not audio_file.exists():
        raise HTTPException(status_code=404, detail=f"未找到 {date} 的音频文件")
    return FileResponse(
        path=str(audio_file),
        media_type="audio/mpeg",
        filename=f"{date}.mp3",
    )

def main():
    import os
    port = int(os.getenv("PORT", 8000))
    # 强烈建议使用字符串格式，更稳定
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()
