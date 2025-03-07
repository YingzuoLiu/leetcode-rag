from abc import ABC, abstractmethod
from typing import List, Dict, Any

class KnowledgeBase(ABC):
    """知识库基类"""
    
    @abstractmethod
    def load(self) -> bool:
        """加载知识库数据"""
        pass
    
    @abstractmethod
    def get_items(self, category: str = None) -> List[Dict[str, Any]]:
        """获取知识条目"""
        pass
    
    @abstractmethod
    def get_item_by_id(self, item_id: str) -> Dict[str, Any]:
        """根据ID获取知识条目"""
        pass