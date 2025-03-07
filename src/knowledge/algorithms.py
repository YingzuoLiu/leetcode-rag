import json
import os
from typing import List, Dict, Any
from pathlib import Path
from src.config import KNOWLEDGE_DIR
from src.knowledge.base import KnowledgeBase

class AlgorithmKnowledge(KnowledgeBase):
    """算法知识库"""
    
    def __init__(self):
        self.algorithms = []
        self.data_structures = []
        self.algorithms_path = KNOWLEDGE_DIR / "algorithms.json"
        self.data_structures_path = KNOWLEDGE_DIR / "data_structures.json"
    
    def load(self) -> bool:
        """加载算法和数据结构知识"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.algorithms_path), exist_ok=True)
            
            # 加载算法
            if self.algorithms_path.exists():
                with open(self.algorithms_path, 'r', encoding='utf-8') as f:
                    self.algorithms = json.load(f)
            else:
                # 创建基础算法数据
                self._create_base_algorithms()
                
            # 加载数据结构
            if self.data_structures_path.exists():
                with open(self.data_structures_path, 'r', encoding='utf-8') as f:
                    self.data_structures = json.load(f)
            else:
                # 创建基础数据结构数据
                self._create_base_data_structures()
                
            return True
        except Exception as e:
            print(f"加载知识库失败: {str(e)}")
            return False
    
    def get_items(self, category: str = None) -> List[Dict[str, Any]]:
        """获取知识条目"""
        if category == "algorithms":
            return self.algorithms
        elif category == "data_structures":
            return self.data_structures
        else:
            # 返回所有知识
            return self.algorithms + self.data_structures
    
    def get_item_by_id(self, item_id: str) -> Dict[str, Any]:
        """根据ID获取知识条目"""
        # 搜索算法
        for algo in self.algorithms:
            if algo.get('id') == item_id:
                return algo
        
        # 搜索数据结构
        for ds in self.data_structures:
            if ds.get('id') == item_id:
                return ds
        
        return {}
    
    def _create_base_algorithms(self):
        """创建基础算法数据"""
        base_algorithms = [
            {
                "id": "two-pointer",
                "name": "双指针技术",
                "category": "algorithms",
                "description": "使用两个指针在数组或链表上移动，通常用于查找对、子数组等",
                "applications": ["数组", "链表", "字符串"],
                "complexity": "时间 O(n), 空间 O(1)",
                "example": "用于求解数组中的两数之和等问题",
                "keywords": ["双指针", "two pointer", "滑动", "sliding"]
            },
            {
                "id": "binary-search",
                "name": "二分查找",
                "category": "algorithms",
                "description": "在有序集合中查找特定元素的高效算法",
                "applications": ["有序数组", "搜索", "旋转数组"],
                "complexity": "时间 O(log n), 空间 O(1)",
                "example": "在排序数组中查找元素位置",
                "keywords": ["二分", "binary search", "折半", "查找"]
            },
            {
                "id": "dynamic-programming",
                "name": "动态规划",
                "category": "algorithms",
                "description": "将问题分解为子问题并存储子问题的解，避免重复计算",
                "applications": ["优化问题", "计数问题", "最大/最小值问题"],
                "complexity": "时间和空间复杂度取决于状态数量和转移",
                "example": "背包问题，最长公共子序列等",
                "keywords": ["动态规划", "DP", "dynamic programming", "最优子结构"]
            },
            {
                "id": "greedy",
                "name": "贪心算法",
                "category": "algorithms",
                "description": "在每一步选择中都采取当前状态下最好的选择",
                "applications": ["区间问题", "排序问题", "图算法"],
                "complexity": "通常时间 O(n log n), 空间 O(1)",
                "example": "区间调度问题，哈夫曼编码",
                "keywords": ["贪心", "greedy", "局部最优"]
            }
        ]
        
        self.algorithms = base_algorithms
        
        # 保存到文件
        with open(self.algorithms_path, 'w', encoding='utf-8') as f:
            json.dump(base_algorithms, f, ensure_ascii=False, indent=2)
    
    def _create_base_data_structures(self):
        """创建基础数据结构数据"""
        base_data_structures = [
            {
                "id": "hash-table",
                "name": "哈希表",
                "category": "data_structures",
                "description": "通过键值映射存储数据，提供O(1)的查找时间",
                "operations": "插入O(1), 查找O(1), 删除O(1)",
                "python_implementation": "dict, Counter, defaultdict",
                "use_cases": "查找、计数、缓存结果等",
                "keywords": ["哈希表", "hash table", "字典", "dict", "map"]
            },
            {
                "id": "heap",
                "name": "堆/优先队列",
                "category": "data_structures",
                "description": "特殊的树形数据结构，可以高效获取最大/最小元素",
                "operations": "插入O(log n), 获取最值O(1), 删除最值O(log n)",
                "python_implementation": "heapq模块, PriorityQueue",
                "use_cases": "Top K问题，调度问题等",
                "keywords": ["堆", "heap", "优先队列", "priority queue", "最大堆", "最小堆"]
            },
            {
                "id": "tree",
                "name": "树",
                "category": "data_structures",
                "description": "由节点和边组成的分层数据结构",
                "operations": "插入O(log n), 查找O(log n), 删除O(log n)（平衡树）",
                "python_implementation": "自定义类",
                "use_cases": "层次结构表示, 搜索, 排序",
                "keywords": ["树", "tree", "二叉树", "binary tree", "平衡树"]
            }
        ]
        
        self.data_structures = base_data_structures
        
        # 保存到文件
        with open(self.data_structures_path, 'w', encoding='utf-8') as f:
            json.dump(base_data_structures, f, ensure_ascii=False, indent=2)