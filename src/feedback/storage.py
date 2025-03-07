import os
import json
import time
import hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.config import FEEDBACK_DIR

class FeedbackStorage:
    """简化的反馈存储系统 - 使用JSON文件存储"""
    
    def __init__(self):
        """初始化反馈存储"""
        self.problems_dir = FEEDBACK_DIR / "problems"
        self.solutions_dir = FEEDBACK_DIR / "solutions"
        self.feedback_dir = FEEDBACK_DIR / "feedback"
        self.index_path = FEEDBACK_DIR / "index.json"
        
        # 确保目录存在
        self.problems_dir.mkdir(parents=True, exist_ok=True)
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载或创建索引
        self.index = self._load_or_create_index()
    
    def _load_or_create_index(self) -> Dict[str, Any]:
        """加载或创建索引文件"""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            index = {
                "problems": {},
                "solutions": {},
                "feedback": {},
                "problem_features": {}  # 用于快速检索相似问题
            }
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
            return index
    
    def _save_index(self):
        """保存索引文件"""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _generate_hash(self, text: str) -> str:
        """生成文本的哈希值作为ID"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def add_problem(self, problem_text: str, features: Dict[str, Any]) -> str:
        """添加问题"""
        # 生成ID
        problem_id = self._generate_hash(problem_text)
        
        # 如果问题已存在，直接返回ID
        if problem_id in self.index["problems"]:
            return problem_id
        
        # 保存问题文件
        problem_data = {
            "id": problem_id,
            "text": problem_text,
            "features": features,
            "created_at": time.time()
        }
        
        with open(self.problems_dir / f"{problem_id}.json", 'w', encoding='utf-8') as f:
            json.dump(problem_data, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self.index["problems"][problem_id] = {
            "id": problem_id,
            "created_at": problem_data["created_at"]
        }
        
        # 将特征添加到特征索引中，用于后续相似性搜索
        self.index["problem_features"][problem_id] = {
            "problem_type": features.get("problem_type", ""),
            "difficulty": features.get("difficulty", ""),
            "data_structures": features.get("data_structures", []),
            "algorithms": features.get("algorithms", [])
        }
        
        self._save_index()
        return problem_id
    
    def add_solution(self, problem_id: str, code: str, language: str, reasoning: str) -> str:
        """添加解决方案"""
        # 生成ID
        solution_id = self._generate_hash(f"{problem_id}:{code}")
        
        # 如果解决方案已存在，直接返回ID
        if solution_id in self.index["solutions"]:
            return solution_id
        
        # 保存解决方案文件
        solution_data = {
            "id": solution_id,
            "problem_id": problem_id,
            "code": code,
            "language": language,
            "reasoning": reasoning,
            "created_at": time.time()
        }
        
        with open(self.solutions_dir / f"{solution_id}.json", 'w', encoding='utf-8') as f:
            json.dump(solution_data, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self.index["solutions"][solution_id] = {
            "id": solution_id,
            "problem_id": problem_id,
            "language": language,
            "created_at": solution_data["created_at"]
        }
        
        self._save_index()
        return solution_id
    
    def add_feedback(self, solution_id: str, is_positive: bool, comment: str = None) -> str:
        """添加反馈"""
        # 生成ID
        feedback_id = f"{solution_id}_{int(time.time())}"
        
        # 保存反馈文件
        feedback_data = {
            "id": feedback_id,
            "solution_id": solution_id,
            "is_positive": is_positive,
            "comment": comment,
            "created_at": time.time()
        }
        
        with open(self.feedback_dir / f"{feedback_id}.json", 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self.index["feedback"][feedback_id] = {
            "id": feedback_id,
            "solution_id": solution_id,
            "is_positive": is_positive,
            "created_at": feedback_data["created_at"]
        }
        
        self._save_index()
        return feedback_id
    
    def get_problem(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """获取问题"""
        problem_path = self.problems_dir / f"{problem_id}.json"
        if not problem_path.exists():
            return None
        
        with open(problem_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_solution(self, solution_id: str) -> Optional[Dict[str, Any]]:
        """获取解决方案"""
        solution_path = self.solutions_dir / f"{solution_id}.json"
        if not solution_path.exists():
            return None
        
        with open(solution_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_feedback_for_solution(self, solution_id: str) -> List[Dict[str, Any]]:
        """获取特定解决方案的所有反馈"""
        feedbacks = []
        
        # 从索引中找到与解决方案相关的反馈
        for feedback_id, feedback_info in self.index["feedback"].items():
            if feedback_info["solution_id"] == solution_id:
                feedback_path = self.feedback_dir / f"{feedback_id}.json"
                if feedback_path.exists():
                    with open(feedback_path, 'r', encoding='utf-8') as f:
                        feedbacks.append(json.load(f))
        
        # 按时间排序
        feedbacks.sort(key=lambda x: x["created_at"], reverse=True)
        return feedbacks
    
    def get_similar_problems(self, features: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """获取具有相似特征的问题"""
        problem_scores = []
        
        # 计算每个问题的相似度得分
        for problem_id, problem_features in self.index["problem_features"].items():
            score = self._calculate_similarity(features, problem_features)
            problem_scores.append((problem_id, score))
        
        # 按相似度排序
        problem_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 获取前N个相似问题
        similar_problems = []
        for problem_id, score in problem_scores[:limit]:
            problem = self.get_problem(problem_id)
            if problem:
                problem["similarity_score"] = score
                similar_problems.append(problem)
        
        return similar_problems
    
    def _calculate_similarity(self, features1: Dict[str, Any], features2: Dict[str, Any]) -> float:
        """计算两组特征之间的相似度（简单实现）"""
        score = 0.0
        
        # 问题类型相似度
        if features1.get('problem_type') == features2.get('problem_type'):
            score += 3.0
        
        # 难度相似度
        if features1.get('difficulty') == features2.get('difficulty'):
            score += 1.0
        
        # 数据结构相似度
        data_structures1 = set(features1.get('data_structures', []))
        data_structures2 = set(features2.get('data_structures', []))
        if data_structures1 and data_structures2:
            overlap = len(data_structures1.intersection(data_structures2))
            score += overlap * 2.0
        
        # 算法相似度
        algorithms1 = set(features1.get('algorithms', []))
        algorithms2 = set(features2.get('algorithms', []))
        if algorithms1 and algorithms2:
            overlap = len(algorithms1.intersection(algorithms2))
            score += overlap * 2.0
        
        return score
    
    def get_feedback_statistics(self) -> Dict[str, Any]:
        """获取反馈统计信息"""
        total_problems = len(self.index["problems"])
        total_solutions = len(self.index["solutions"])
        total_feedback = len(self.index["feedback"])
        
        positive_feedback = sum(1 for info in self.index["feedback"].values() if info["is_positive"])
        negative_feedback = total_feedback - positive_feedback
        
        positive_rate = positive_feedback / total_feedback if total_feedback > 0 else 0
        
        return {
            "total_problems": total_problems,
            "total_solutions": total_solutions,
            "total_feedback": total_feedback,
            "positive_feedback": positive_feedback,
            "negative_feedback": negative_feedback,
            "positive_rate": positive_rate
        }