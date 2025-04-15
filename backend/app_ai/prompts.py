# AI分析提示模板

# 系统提示模板
SYSTEM_PROMPT = """你是一个Verilog硬件描述语言专家，擅长分析和调试Verilog代码中的错误。
你需要根据提供的信息，帮助学生找出Verilog代码中的问题，并给出详细解释和修改建议。
请注意语言简洁、分析准确，重点突出错误原因和解决方案。"""

# 用户提示模板
def generate_user_prompt(
    problem_title, 
    problem_description, 
    testbench_code, 
    reference_code, 
    user_code, 
    log_content, 
    waveform=None, 
    error_code=None
):
    """
    生成分析代码的用户提示
    
    参数:
    - problem_title: 题目标题
    - problem_description: 题目描述
    - testbench_code: 测试台代码
    - reference_code: 参考实现代码
    - user_code: 用户提交的代码
    - log_content: 仿真日志内容
    - waveform: 波形文件内容（可选）
    - error_code: 错误代码（可选）
    
    返回:
    - 格式化的提示字符串
    """
    
    error_type = ""
    if error_code:
        error_types = {
            "ERROR_COMPILE_FAIL": "编译错误，可能存在语法问题",
            "ERROR_SIM_LOAD_FAIL": "仿真加载失败",
            "ERROR_SIM_RUN_FAIL": "仿真运行失败",
            "ERROR_SIM_TIMEOUT": "仿真超时",
            "ERROR_MISMATCH": "输出结果不匹配",
            "ERROR_UNKNOWN": "未知错误"
        }
        error_type = error_types.get(error_code, "未知错误类型")
    
    # 构建提示
    prompt = f"""我需要你帮忙分析一段Verilog代码中的问题。

## 题目信息
标题: {problem_title}
描述: {problem_description}

## 错误信息
错误类型: {error_type}

## 测试代码
```verilog
{testbench_code}
```

## 参考实现
```verilog
{reference_code}
```

## 用户提交的代码
```verilog
{user_code}
```

## 仿真日志
```
{log_content[:2000]}
```
"""
    
    # 如果有波形数据，添加到提示中（但限制长度）
    if waveform and len(waveform) > 0:
        waveform_sample = waveform[:300] + "... [波形数据过长已截断]"
        prompt += f"""
## 波形数据（VCD格式的摘要）
```
{waveform_sample}
```
"""
    
    prompt += """
请详细分析代码中存在的问题，并给出具体的修改建议：
1. 错误的确切位置和原因
2. 如何修复这些错误的具体建议
3. 可能的优化方向（如有）

你的回答需要简洁明了，重点突出问题根源和解决方案。
"""
    
    return prompt 