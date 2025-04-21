# 学习路径数据结构
learning_paths = {
    1: {
        "id": 1,
        "name": "Verilog基础入门",
        "description": "从零开始学习Verilog HDL语言基础",
        "start_problem_id": 1  # 起始题目ID
    },
    2: {
        "id": 2,
        "name": "数字电路设计进阶",
        "description": "学习更复杂的数字电路设计技巧",
        "start_problem_id": 5  # 起始题目ID
    }
    # 可以添加更多学习路径
}

def get_learning_path(path_id):
    """获取指定ID的学习路径"""
    return learning_paths.get(path_id)

def get_all_learning_paths():
    """获取所有学习路径"""
    return list(learning_paths.values())

def add_learning_path(name, description, start_problem_id):
    """添加新的学习路径"""
    new_id = max(learning_paths.keys()) + 1 if learning_paths else 1
    learning_paths[new_id] = {
        "id": new_id,
        "name": name,
        "description": description,
        "start_problem_id": start_problem_id
    }
    return new_id