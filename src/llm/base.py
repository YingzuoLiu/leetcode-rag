from abc import ABC, abstractmethod
from typing import Dict, Any

class LLM(ABC):
    """语言模型基类"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass
    
    @abstractmethod
    def extract_features(self, text: str) -> Dict[str, Any]:
        """提取特征"""
        pass