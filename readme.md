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

```
# Update RLHF 

# 双循环优化架构

## 前台用户反馈循环

```
                    ┌───────────────────────────────┐
                    │       前台用户反馈循环         │
                    │    (贪心式实时学习RLHF)        │
                    └───────────┬────────────┬──────┘
                                │            │
                                ▼            │
┌─────────────┐     ┌─────────────────┐      │     ┌─────────────────┐
│  LeetCode   │     │                 │      │     │                 │
│    问题     │────▶│   代码生成系统   │◀─────┴────▶│  用户反馈(👍/👎) │
└─────────────┘     │                 │            │                 │
                    └────────┬────────┘            └─────────────────┘
                             │
                             │ 多样性
                             │ 解决方案
                             ▼
                    ┌──────────────────────────────┐
                    │      后台人工标注微调循环     │
                    │      (模型深度优化RLHF)      │
                    └──────────────────────────────┘
```

### **前台用户反馈循环（已实现）**

#### **用户提交问题**
- LeetCode 算法问题输入
- 可选编程语言选择

#### **系统生成解决方案**
- 使用 RAG 检索相关算法知识
- 基于反馈记忆增强提示
- 生成初始解决方案

#### **用户提供简单反馈**
- 直观的 👍/👎 反馈机制
- 无需详细文本评论

#### **即时学习**
- 反馈立即存入记忆库
- 使用语义相似性索引
- 为未来提供学习经验

---

## 后台人工标注微调循环（待实现）

#### **多样性解决方案生成**
- 为同一问题生成 5-10 个不同解法
- 使用不同温度参数和算法提示
- 确保解法多样性（贪心、DP、分治等）

#### **专家标注排名**
- 算法专家对解决方案进行排序
- 考虑正确性、效率、可读性、简洁性等
- 收集详细评价和改进建议

#### **偏好数据构建**
- 将排名转化为成对偏好数据
- 构建高质量训练数据集
- 定期更新数据集

#### **模型微调**
- 使用 LoRA 进行参数高效微调
- 应用 DPO 算法基于排名进行训练
- 定期发布微调模型





