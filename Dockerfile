FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

WORKDIR /app

# 安装Python和依赖
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
# 安装依赖
RUN pip3 install --no-cache-dir --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

# 创建目录结构
RUN mkdir -p /app/models /app/data/knowledge_base /app/data/embeddings /app/data/feedback/problems /app/data/feedback/solutions /app/data/feedback/feedback

# 复制项目文件
COPY . .

# 暴露服务端口
EXPOSE 8000

# 启动命令
CMD ["python3", "app.py"]