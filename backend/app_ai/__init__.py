"""
AI分析模块初始化文件
提供对外接口和服务
"""

from .deepseek_api import deepseek_api, DeepseekAPI
from .prompts import generate_user_prompt, SYSTEM_PROMPT

# 导入路由模块，确保蓝图被注册
from . import routes 