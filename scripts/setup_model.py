"""
下载DeepSeek-Coder模型（简化版，无量化）
"""
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import sys

# 减少日志输出
from transformers.utils import logging as transformers_logging
transformers_logging.set_verbosity_error()

def download_model(model_name, output_dir):
    """下载模型（无量化）"""
    print(f"正在下载模型：{model_name}")
    
    # 下载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.save_pretrained(output_dir)
    print("Tokenizer已保存")
    
    # 检查GPU是否可用
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    
    # 下载模型（CPU版本，无量化）
    print("下载模型（这可能需要一些时间）...")
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # 使用半精度而不是量化
            low_cpu_mem_usage=False,    # 禁用需要加速库的功能
            trust_remote_code=True
        )
        
        # 保存模型
        model.save_pretrained(output_dir)
        print(f"模型已保存到: {output_dir}")
        return True
    except Exception as e:
        print(f"下载模型时出错: {str(e)}")
        return False

if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目根目录
    base_dir = os.path.dirname(script_dir)
    # 设置模型目录
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # 选择模型
    model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
    output_dir = os.path.join(models_dir, "deepseek-coder-1.3b-instruct")
    
    success = download_model(model_name, output_dir)
    if success:
        print("模型下载完成！系统准备就绪。")
    else:
        print("模型下载失败。请检查网络连接并重试。")