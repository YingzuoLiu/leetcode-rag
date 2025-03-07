import re
import os
import torch
from typing import Dict, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.config import DEFAULT_MODEL_PATH
from src.llm.base import LLM

class DeepSeekLLM(LLM):
    """DeepSeek-Coder 本地LLM实现"""
    
    def __init__(self, model_path: str = None):
        """初始化DeepSeek-Coder模型"""
        self.model_path = model_path or DEFAULT_MODEL_PATH
        
        if not os.path.exists(self.model_path):
            raise ValueError(f"模型路径不存在: {self.model_path}，请先运行下载脚本")
        
        # 加载模型和tokenizer
        print(f"正在加载DeepSeek-Coder模型: {self.model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16
        )
        
        # 设置设备
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"DeepSeek-Coder 已加载到 {self.device}")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """生成文本"""
        try:
            # 设置DeepSeek-Coder的聊天模板
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            # 处理输入为模型格式
            input_text = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            
            # 编码输入
            inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)
            
            # 生成响应
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.95,
                    do_sample=(temperature > 0.1),
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # 解码输出
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 提取模型回复部分
            response = generated_text[len(input_text):].strip()
            
            return response
        except Exception as e:
            print(f"DeepSeek-Coder 生成失败: {str(e)}")
            return f"生成失败: {str(e)}"
    
    def extract_features(self, text: str) -> Dict[str, Any]:
        """提取问题特征"""
        prompt = f"""
分析以下LeetCode问题，提取关键特征:

{text}

请以JSON格式返回以下字段:
1. problem_type: 问题类型（如数组、字符串、树等）
2. difficulty: 难度（简单、中等、困难）
3. data_structures: 可能涉及的数据结构（数组形式）
4. algorithms: 可能适用的算法（数组形式）

仅返回JSON格式，不要有其他文字。
"""
        try:
            response = self.generate(prompt, temperature=0.1)
            # 尝试从回复中提取JSON
            import json
            
            # 查找JSON块
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # 尝试直接解析
            try:
                return json.loads(response)
            except:
                # 尝试提取可能是JSON的部分
                json_like = re.search(r'\{.*\}', response, re.DOTALL)
                if json_like:
                    return json.loads(json_like.group(0))
            
            # 如果无法提取，返回默认值
            return {
                "problem_type": "unknown",
                "difficulty": "medium",
                "data_structures": [],
                "algorithms": []
            }
        except Exception as e:
            print(f"特征提取失败: {str(e)}")
            return {
                "problem_type": "unknown",
                "difficulty": "medium",
                "data_structures": [],
                "algorithms": []
            }