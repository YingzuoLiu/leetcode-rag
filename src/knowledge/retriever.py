import os
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDINGS_DIR, DEFAULT_EMBEDDING_MODEL
from src.knowledge.algorithms import AlgorithmKnowledge

# 尝试导入faiss，如果失败则尝试导入CPU版本
try:
    import faiss
except ImportError:
    try:
        import faiss.contrib.faiss_contrib as faiss
    except ImportError:
        raise ImportError("无法导入faiss。请安装faiss-cpu或faiss-gpu。")

class KnowledgeRetriever:
    """知识检索器"""
    
    def __init__(self, embedding_model: str = None):
        # 加载知识库
        self.knowledge_base = AlgorithmKnowledge()
        self.knowledge_base.load()
        
        # 加载嵌入模型
        self.embedding_model = embedding_model or DEFAULT_EMBEDDING_MODEL
        self.model = SentenceTransformer(self.embedding_model)
        
        # 索引路径
        self.index_path = os.path.join(EMBEDDINGS_DIR, "knowledge_index.faiss")
        self.items_path = os.path.join(EMBEDDINGS_DIR, "knowledge_items.npy")
        
        # 初始化索引
        self.index = None
        self.items = []
        
        # 加载或创建索引
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """加载或创建知识索引"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        # 检查是否有现有索引
        if os.path.exists(self.index_path) and os.path.exists(self.items_path):
            try:
                # 加载现有索引
                self.index = faiss.read_index(self.index_path)
                self.items = np.load(self.items_path, allow_pickle=True).tolist()
                print(f"成功加载索引: {self.index_path}")
            except Exception as e:
                print(f"加载索引失败: {str(e)}")
                self._create_index()
        else:
            # 创建新索引
            self._create_index()
    
    def _create_index(self):
        """创建知识索引"""
        try:
            # 获取所有知识条目
            all_items = self.knowledge_base.get_items()
            self.items = all_items
            
            # 准备文本用于嵌入
            texts = []
            for item in all_items:
                # 组合多个字段以提高匹配质量
                text = f"{item.get('name', '')} {item.get('description', '')} {' '.join(item.get('keywords', []))}"
                texts.append(text)
            
            print(f"为{len(texts)}个知识条目生成嵌入...")
            
            # 生成嵌入
            embeddings = self.model.encode(texts)
            
            # 创建索引
            dimension = embeddings.shape[1]
            print(f"创建维度为{dimension}的索引")
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(np.array(embeddings).astype('float32'))
            
            # 保存索引和条目
            faiss.write_index(self.index, self.index_path)
            np.save(self.items_path, np.array(self.items, dtype=object))
            print(f"索引已保存到: {self.index_path}")
        except Exception as e:
            print(f"创建索引失败: {str(e)}")
            # 创建一个空索引以确保程序可以继续运行
            self.items = []
            dimension = 384  # SentenceTransformer默认维度
            self.index = faiss.IndexFlatL2(dimension)
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """检索相关知识"""
        if not self.items or self.index is None:
            print("警告: 索引未正确初始化，返回空结果")
            return []
            
        try:
            # 生成查询嵌入
            query_embedding = self.model.encode([query])
            
            # 搜索最近邻
            distances, indices = self.index.search(query_embedding.astype('float32'), min(k, len(self.items)))
            
            # 整理结果
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.items):
                    item = self.items[idx]
                    results.append({
                        'item': item,
                        'score': float(1.0 / (1.0 + distances[0][i]))  # 转换距离为相似度分数
                    })
            
            return results
        except Exception as e:
            print(f"检索失败: {str(e)}")
            return []