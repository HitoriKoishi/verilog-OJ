# DeepSeek API配置文件
import os
from pathlib import Path
from dotenv import load_dotenv

# 默认API密钥（仅用于开发环境）
DEFAULT_API_KEY = "your-deepseek-api-key"

# 尝试从.env文件加载API密钥
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
api_key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api_keys.txt')

# 首先尝试从专用的api_keys.txt文件加载
api_key = None
try:
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r', encoding='utf-8') as f:  # 明确指定UTF-8编码
            api_key = f.read().strip()
            if api_key:
                print("已从api_keys.txt加载DeepSeek API密钥")
            else:
                print("警告: api_keys.txt文件存在但为空")
    else:
        print("警告: api_keys.txt文件不存在，尝试从环境变量加载")
except Exception as e:
    print(f"读取api_keys.txt时出错: {e}")

# 如果专用文件加载失败，尝试从.env文件或环境变量加载
if not api_key:
    # 尝试加载.env文件
    if os.path.exists(env_path):
        load_dotenv(env_path)
        
    # 从环境变量获取API密钥
    api_key = os.environ.get("DEEPSEEK_API_KEY", DEFAULT_API_KEY)
    
    if api_key == DEFAULT_API_KEY:
        print("警告: 未找到DeepSeek API密钥，使用默认值。AI分析功能将无法正常工作。")
        print("请在项目根目录创建api_keys.txt文件并添加您的API密钥，或在.env文件中设置DEEPSEEK_API_KEY。")

# 设置最终的API密钥和其他配置
DEEPSEEK_API_KEY = api_key
# DeepSeek API基础URL
DEEPSEEK_API_BASE_URL = "https://api.deepseek.com"
# DeepSeek模型名称
DEEPSEEK_MODEL = "deepseek-chat" 