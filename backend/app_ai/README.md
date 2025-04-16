# DeepSeek AI 分析模块

本模块为Veri-OJ系统提供基于DeepSeek LLM的代码分析功能，帮助学生更好地理解代码错误并提供修改建议。

## 功能说明

- 对失败的代码提交进行智能分析
- 提供错误原因解释
- 给出具体修改建议
- 分析代码优化空间

## 安装配置

### 1. 安装依赖

确保已安装所需的Python包：

```bash
pip install openai==1.6.0 python-dotenv==0.19.0
```

或直接安装项目所有依赖：

```bash
pip install -r requirements.txt
```

### 2. API密钥配置

AI分析功能需要DeepSeek API密钥才能正常工作。有两种方式配置密钥：

#### 方式一：创建api_keys.txt文件（推荐）

1. 在项目根目录创建`api_keys.txt`文件
2. 将您的DeepSeek API密钥粘贴到该文件中
3. 确保此文件已添加到`.gitignore`中，不会被提交到版本控制系统

示例：
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 方式二：使用环境变量

1. 在项目根目录创建`.env`文件
2. 添加以下内容：
   ```
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. 确保该文件已添加到`.gitignore`中

## API接口

### 1. 分析提交的代码

**URL**: `GET /ai/analyze/<submission_id>`

**描述**: 分析指定ID的提交记录，返回AI分析结果。

**参数**:
- `submission_id`: 提交记录的ID

**响应**:
```json
{
  "success": true,
  "analysis": "分析结果的Markdown文本内容..."
}
```

**错误响应**:
```json
{
  "error": "错误信息"
}
```

## 使用流程

1. 学生提交Verilog代码进行评测
2. 如果评测失败，前端界面会自动显示"AI智能分析"按钮
3. 点击按钮后，系统会向DeepSeek API发送包含题目信息、错误代码、参考代码、测试用例等信息的请求
4. DeepSeek API分析后返回结果，显示在页面上

## 技术实现

该模块使用OpenAI兼容的API格式与DeepSeek进行通信，通过精心设计的提示模板构建高质量分析请求。

主要组件：
- `config.py`: 配置文件，负责加载API密钥和设置
- `prompts.py`: 提示模板，构建发送给AI的提示内容
- `deepseek_api.py`: API调用实现
- `routes.py`: Flask路由处理

## 注意事项

- 该模块依赖DeepSeek API服务，请确保网络连接畅通
- API调用可能产生费用，请合理使用
- 分析结果仅供参考，最终判断应由教师或学生自行做出
- AI分析功能仅对评测失败的提交可用 