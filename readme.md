# LeetCode RAG系统

使用检索增强生成（RAG）和Chain-of-Thought（CoT）方法解决LeetCode问题的辅助系统。

## 功能特点

- 使用DeepSeek-Coder模型生成高质量代码解决方案
- 基于相似性检索算法知识库
- 支持用户反馈和解决方案改进
- 自动代码执行和验证

## 安装步骤

克隆仓库
   ```bash
   git clone https://github.com/YingzuoLiu/leetcode-rag.git
   cd leetcode-rag

安装依赖
bashCopypip install -r requirements.txt

下载模型
bashCopypython scripts/setup_model.py

运行应用
bashCopypython app.py

在浏览器中访问 http://localhost:8000


## 项目结构

data/：知识库和嵌入数据
models/：语言模型
src/：源代码
public/：前端资源
scripts/：辅助脚本

