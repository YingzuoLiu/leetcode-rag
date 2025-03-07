import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from src.config import HOST, PORT, ENVIRONMENT
from src.api.routes import router

# 创建应用
app = FastAPI(
    title="LeetCode RAG助手",
    description="使用检索增强生成和Chain-of-Thought方法解决LeetCode问题",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(router, prefix="/api")

# 添加静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 主页路由
@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_file = Path("static/index.html")
    if html_file.exists():
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    else:
        return "欢迎使用LeetCode RAG助手！请先创建static/index.html文件。"

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"发生错误: {str(exc)}"}
    )

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # 启动服务
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=ENVIRONMENT == "development"
    )