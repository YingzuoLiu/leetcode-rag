from fastapi import APIRouter, HTTPException
from src.api.models import ProblemRequest, SolutionResponse, FeedbackRequest, FeedbackResponse
from src.llm.deepseek import DeepSeekLLM
from src.knowledge.retriever import KnowledgeRetriever
from src.llm.cot import ChainOfThoughtReasoner
from src.feedback.storage import FeedbackStorage
from src.feedback.learner import FeedbackLearner
import time

router = APIRouter()

# 初始化组件
llm = DeepSeekLLM()
retriever = KnowledgeRetriever()
reasoner = ChainOfThoughtReasoner(llm, retriever)
feedback_storage = FeedbackStorage()
feedback_learner = FeedbackLearner(llm, retriever, feedback_storage)

@router.post("/solve", response_model=SolutionResponse)
async def solve_problem(request: ProblemRequest):
    """解决LeetCode问题"""
    try:
        start_time = time.time()
        
        # 提取问题特征
        features = llm.extract_features(request.problem)
        
        # 存储问题到存储
        problem_id = feedback_storage.add_problem(request.problem, features)
        
        # 增强提示（添加历史反馈）
        history_prompt = feedback_learner.enhance_prompt_with_history(request.problem, features)
        # TODO: 将history_prompt添加到reasoner.generate_solution中
        
        # 生成解决方案
        solution = reasoner.generate_solution(request.problem, request.language)
        
        # 存储解决方案
        solution_id = feedback_storage.add_solution(
            problem_id, 
            solution["code"], 
            request.language, 
            solution["reasoning"]
        )
        
        # 计算总耗时
        total_time = time.time() - start_time
        print(f"总处理时间: {total_time:.2f}秒")
        
        return {
            "code": solution["code"],
            "reasoning": solution["reasoning"],
            "features": solution["features"],
            "solution_id": solution_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """提交代码反馈"""
    try:
        # 获取解决方案
        solution = feedback_storage.get_solution(request.solution_id)
        if not solution:
            raise HTTPException(status_code=404, detail="解决方案不存在")
        
        # 添加反馈
        feedback_id = feedback_storage.add_feedback(
            request.solution_id,
            request.is_positive,
            request.comment
        )
        
        return {
            "id": feedback_id,
            "solution_id": request.solution_id,
            "success": True,
            "message": "反馈提交成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交反馈失败: {str(e)}")

@router.get("/stats")
async def get_stats():
    """获取系统统计信息"""
    try:
        stats = feedback_storage.get_feedback_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")