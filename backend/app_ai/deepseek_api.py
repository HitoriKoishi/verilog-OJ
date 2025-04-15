"""
DeepSeek AI API调用模块
实现与DeepSeek API的交互
"""

import os
import json
import sys
import traceback
from openai import OpenAI
from .config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE_URL, DEEPSEEK_MODEL
from .prompts import SYSTEM_PROMPT, generate_user_prompt

class DeepseekAPI:
    """DeepSeek API调用类"""
    
    def __init__(self, api_key=None, base_url=None, model=None):
        """
        初始化DeepSeek API客户端
        
        参数:
        - api_key: API密钥，默认使用配置文件中的密钥
        - base_url: API基础URL，默认使用配置文件中的URL
        - model: 使用的模型，默认使用配置文件中的模型
        """
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.base_url = base_url or DEEPSEEK_API_BASE_URL
        self.model = model or DEEPSEEK_MODEL
        
        print(f"初始化DeepSeek API客户端，使用URL: {self.base_url}，模型: {self.model}")
        
        # 检查API密钥是否有效
        if not self.api_key or self.api_key == "your-deepseek-api-key":
            print("错误: 无效的API密钥")
            self.client = None
            return
            
        # 初始化OpenAI客户端，仅使用兼容的参数
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            print("DeepSeek API客户端初始化成功，准备好发送请求")
            self.client_ready = True
        except Exception as e:
            print(f"初始化DeepSeek API客户端失败: {e}")
            traceback.print_exc(file=sys.stdout)
            self.client = None
            self.client_ready = False
    
    def analyze_code(self, 
                    problem_title, 
                    problem_description, 
                    testbench_code, 
                    reference_code, 
                    user_code, 
                    log_content, 
                    waveform=None, 
                    error_code=None,
                    stream=False):
        """
        分析代码并获取AI反馈
        
        参数:
        - problem_title: 题目标题
        - problem_description: 题目描述
        - testbench_code: 测试台代码
        - reference_code: 参考实现代码
        - user_code: 用户提交的代码
        - log_content: 仿真日志内容
        - waveform: 波形文件内容（可选）
        - error_code: 错误代码（可选）
        - stream: 是否使用流式响应，默认为False
        
        返回:
        - AI分析结果
        """
        try:
            # 检查客户端是否初始化成功
            if not self.client or not hasattr(self, 'client_ready') or not self.client_ready:
                return "DeepSeek API客户端初始化失败，无法进行分析。请检查API密钥和网络连接。"
                
            # 生成用户提示
            user_prompt = generate_user_prompt(
                problem_title,
                problem_description,
                testbench_code,
                reference_code,
                user_code,
                log_content,
                waveform,
                error_code
            )
            
            print(f"正在调用DeepSeek API模型 {self.model} 进行代码分析...")
            
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                stream=stream
            )
            
            # 处理响应
            if stream:
                # 返回流式响应对象，由调用者处理
                return response
            else:
                # 返回完整响应内容
                print("DeepSeek API响应成功获取")
                return response.choices[0].message.content
                
        except Exception as e:
            print(f"调用DeepSeek API时出错: {e}")
            traceback.print_exc(file=sys.stdout)
            return f"分析过程中发生错误: {str(e)}\n\n请检查DeepSeek API配置和网络连接。"

# 创建一个全局的API实例以供直接导入使用
deepseek_api = DeepseekAPI() 