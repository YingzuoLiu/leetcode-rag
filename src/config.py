import os
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 环境设置
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 服务设置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# 路径设置
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge_base"
EMBEDDINGS_DIR = BASE_DIR / "data" / "embeddings"
FEEDBACK_DIR = BASE_DIR / "data" / "feedback"
MODELS_DIR = BASE_DIR / "models"

# 模型设置
# 修改这一行
DEFAULT_MODEL_PATH = MODELS_DIR / "deepseek-coder-1.3b-instruct"  # 更小的模型
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# 创建必要的目录
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
os.makedirs(FEEDBACK_DIR / "problems", exist_ok=True)
os.makedirs(FEEDBACK_DIR / "solutions", exist_ok=True)
os.makedirs(FEEDBACK_DIR / "feedback", exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)