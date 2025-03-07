import re
from typing import List, Dict, Any
from src.feedback.storage import FeedbackStorage
from src.llm.base import LLM
from src.knowledge.retriever import KnowledgeRetriever

class FeedbackLearner:
    """反馈学习器 - 从用户反馈中学习改进代码生成"""
    
    def __init__(self, llm: LLM, retriever: KnowledgeRetriever, storage: FeedbackStorage):
        self.llm = llm
        self.retriever = retriever
        self.storage = storage
    
    def enhance_prompt_with_history(self, problem: str, features: Dict[str, Any]) -> str:
        """使用历史反馈增强提示"""
        # 获取相似问题
        similar_problems = self.storage.get_similar_problems(features, limit=3)
        
        if not similar_problems:
            return ""
        
        # 收集反馈见解
        positive_insights = []
        negative_insights = []
        
        for similar_problem in similar_problems:
            problem_id = similar_problem["id"]
            
            # 找出该问题的所有解决方案
            solution_ids = []
            for solution_id, solution_info in self.storage.index["solutions"].items():
                if solution_info["problem_id"] == problem_id:
                    solution_ids.append(solution_id)
            
            for solution_id in solution_ids:
                # 获取该解决方案的反馈
                feedbacks = self.storage.get_feedback_for_solution(solution_id)
                
                for feedback in feedbacks:
                    if feedback["is_positive"] and feedback.get("comment"):
                        positive_insights.append(feedback["comment"])
                    elif not feedback["is_positive"] and feedback.get("comment"):
                        negative_insights.append(feedback["comment"])
        
        # 构建增强提示
        if positive_insights or negative_insights:
            history_prompt = "### 从历史反馈中学到的经验\n\n"
            
            if positive_insights:
                history_prompt += "好的做法:\n"
                for insight in positive_insights[:3]:  # 限制数量
                    history_prompt += f"- ✓ {insight}\n"
            
            if negative_insights:
                if positive_insights:
                    history_prompt += "\n"
                history_prompt += "要避免的问题:\n"
                for insight in negative_insights[:3]:  # 限制数量
                    history_prompt += f"- ✗ {insight}\n"
            
            return history_prompt
        
        return ""