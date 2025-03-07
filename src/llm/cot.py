import re
from typing import List, Dict, Any
from src.llm.base import LLM
from src.knowledge.retriever import KnowledgeRetriever

class ChainOfThoughtReasoner:
    """Chain-of-Thought推理器"""
    
    def __init__(self, llm: LLM, retriever: KnowledgeRetriever):
        self.llm = llm
        self.retriever = retriever
    
    def generate_solution(self, problem: str, language: str = "python") -> Dict[str, Any]:
        """生成解决方案"""
        # 提取问题特征
        features = self.llm.extract_features(problem)
        print(f"提取的问题特征: {features}")
        
        # 检索相关知识
        retrieved_knowledge = self.retriever.retrieve(problem, k=5)
        print(f"检索到 {len(retrieved_knowledge)} 条相关知识")
        
        # 准备CoT提示
        prompt = self._prepare_deepseek_cot_prompt(
            problem, 
            features, 
            retrieved_knowledge, 
            language
        )
        
        # 生成解决方案
        print("生成代码解决方案...")
        response = self.llm.generate(prompt)
        
        # 提取代码
        code = self._extract_code(response, language)
        
        return {
            "code": code,
            "reasoning": response,
            "features": features
        }
    
    def _prepare_deepseek_cot_prompt(self, problem: str, features: Dict[str, Any], 
                                   retrieved_knowledge: List[Dict[str, Any]], 
                                   language: str = "python") -> str:
        """为DeepSeek-Coder准备CoT提示"""
        prompt = f"""
# LeetCode问题解决

## 问题描述
{problem}

## 分析思路
让我一步步解决这个问题：

### 1. 理解问题
这是一个涉及{features.get('problem_type', '算法')}的问题，难度为{features.get('difficulty', '中等')}。
我需要理解输入、输出和约束条件。

### 2. 思考解决方案
"""
        
        # 添加知识库检索结果
        if retrieved_knowledge:
            prompt += "根据相关算法知识，我可以考虑以下几种方法：\n\n"
            for i, item in enumerate(retrieved_knowledge[:3]):
                if 'item' in item and 'name' in item['item']:
                    prompt += f"- **{item['item']['name']}**: {item['item'].get('description', '')}\n"
        
        prompt += """
### 3. 分析复杂度
我需要考虑不同解决方案的时间和空间复杂度，选择最优的方案。

### 4. 设计算法
现在我将设计具体的算法步骤。

### 5. 边界情况
我需要考虑以下边界情况：
- 空输入
- 极端值
- 特殊情况

### 6. 代码实现
下面是{language}实现：
"""
        
        return prompt
    
    def _extract_code(self, response: str, language: str) -> str:
        """从响应中提取代码"""
        pattern = f"```{language}(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # 如果没有找到带有语言标记的代码块，尝试查找任何代码块
        generic_pattern = r"```(.*?)```"
        matches = re.findall(generic_pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        return ""