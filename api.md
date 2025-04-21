# api文档

## [返回](README.md)

## 用户登录

### **URL**
`POST /user/login`

### **描述**
用户登录接口。

### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string"   // 密码
  }
  ```

### **响应**
- 成功
  ```json
  {
  "status": "success",
  "user": {
    "id": 1,
    "username": "test_user",
    "email": "test@example.com"}
    }
  ```

- 失败
  ```json
  {
  "status": "error",
  "message": "需要用户名和密码"
  }
  400
  ```

  ```json
  {
  "status": "error",
  "message": "用户名或密码错误"
  }
  401
  ```

## 用户注销

### **URL**
`GET, POST /user/logout`

### **描述**
用户注销接口。

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
  "status": "success",
  }
  ```


## 登录状态检查

### **URL**
`GET /user/check_auth`

### **描述**
登录状态检查

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "is_login": True,
    "user": {
        "id": 1
        "username": "string"
    }
  }
  ```

  ```json
  {
    "is_login": False
  }
  ```


## 用户注册

### **URL**
`POST /user/register`

### **描述**
用户注册接口。

### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string",   // 密码
    "email": "string"          // 邮箱，可选
  }
  ```

### **响应**
- 成功
  ```json
  {
  "status": "success",
  "user": {
    "id": 1,
    "username": "username",
    "email": "email@example.com"}
    }
  ```

- 失败
  ```json
  {
  "error": "用户名和密码为必填项"
  }
  400
  ```

  ```json
  {
  "error": "用户名已存在"
  }
  409
  ```

  ```json
  {
  "error": "邮箱已被注册"
  }
  409
  ```

## 获取用户资料

### **URL**
`GET /user/profile`

### **描述**
获取用户资料

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "id": 1,
    "username": "username",
    "email": "email@example.com"
  }
  ```

- 失败
  ```json
  {
    "error": "用户不存在"   
  }
  404
  ```

## 更新用户名

### **URL**
`POST /user/update_username`

### **描述**
更新用户名

### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "newUsername": "string"   // 用户名
  }
  ```

### **响应**
- 成功
  ```json
  {
    "status": "success",
    "username": "new_username"
  }
  ```

- 失败
  ```json
  {
    "error": "新用户名不能为空"   
  }
  400
  ```
  ```json
  {
    "error": "该用户名已被使用"   
  }
  409
  ```

## 更新密码

### **URL**
`POST /user/update_password`

### **描述**
更新密码

### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "currentPassword": "string",
    "newPassword": "string"
  }
  ```

### **响应**
- 成功
  ```json
  {
    "status": "success"
  }
  ```

- 失败
  ```json
  {
    "error": "当前密码不正确"   
  }
  401
  ```
  ```json
  {
    "error": "当前密码和新密码不能为空"   
  }
  400
  ```

## 获取Prob列表

### **URL**
`GET /problem/all`

### **描述**
获取问题列表

### **参数**
- 无

### **响应**
  ```json
  [{
    "id": 1,
    "title": "string",
    "difficulty": "string",
    "tags": ["string","string",...],
    "pre_problems": [1, 2, ...],  // 注意：普通用户接口中的 pre_problems 是整数数组
    "next_problems": [1, 2, ...],  // 注意：普通用户接口中的 pre_problems 是整数数组
    "submitted_users_count": 20,
    "passed_users_count": 15,
    **({"is_completed": "未完成"/"已完成"/"失败"/"运行中"} if user_login else {})
  }
  {
    ...
  }]
  ```

## 获取单个Prob详情

### **URL**
`GET /problem/<int:id>`

### **描述**
获取单个Prob详情

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "id": 1,
    "title": "string",
    "document": "md格式文档",
    "difficulty": "string",
    "tags": ["string","string",...],
    "pre_problems": [1, 2, ...],  // 注意：普通用户接口中的 pre_problems 是整数数组
    "next_problems": [1, 2, ...],  // 注意：普通用户接口中的 pre_problems 是整数数组
    "code_template": "string",
    **({"is_completed": "未完成"/"已完成"/"失败"/"运行中"} if user_login else {})
  }
  ```

## 获取用户对各个问题的完成状态

### **URL**
`GET /problem/status`

### **描述**
获取用户对各个问题的完成状态，仅返回问题ID和完成状态

### **参数**
- 无

### **响应**
- 成功
  ```json
  [
      {
          "id": 1,
          "completion_status": "已完成"
      },
      {
          "id": 2,
          "completion_status": "失败"
      },
      {
          "id": 3,
          "completion_status": "仿真中"
      },
      {
          "id": 4,
          "completion_status": "未完成"
      }
      {
        ...
      }
  ]
  ```

## 获取用户对单个问题的提交历史

### **URL**
`GET /problem/<int:id>/submit_history`

### **描述**
获取用户对单个问题的提交历史，返回问题ID，提交时间，完成状态

### **参数**
- 无

### **响应**
- 成功
  ```json
  [
      {
          "submission_id": 123,
          "created_at": "2024-04-15 10:30:00",
          "status": "success"
      },
      {
          "submission_id": 122,
          "created_at": "2024-04-15 10:20:00",
          "status": "failed"
      }
  ]
  ```


## 保存用户代码草稿

### **URL**
`POST /problem/<int:id>/save`

### **描述**
保存用户代码草稿

*此功能需要用户登录*

### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "code": "code"
  }
  ```

### **响应**
- 成功
  ```json
  {
    "status": "success"
  }
  ```

- 失败
  ```json
  {
    "error": "用户或问题不存在"   
  }
  404
  ```

## 获取用户代码草稿

### **URL**
`GET /problem/<int:id>/load`

### **描述**
获取用户代码草稿

*此功能需要用户登录*

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "status": "success",
     "draft_code": "draft_code",
     "draft_time": "updated_at"
  }
  ```
  ```json
  {
    "status": "failed" //用户尚未保存
  }
  ```

- 失败
  ```json
  {
    "error": "用户或问题不存在"   
  }
  404
  ```

## 提交代码，创建提交ID

### **URL**
`POST /problem/<int:id>/submit`

### **描述**
提交代码，创建提交ID

*此功能需要用户登录*

### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "code": "code"
  }
  ```

### **响应**
- 成功
  ```json
  {
    "status": "success",
     "submission_id": 1
  }
  ```

- 失败
  ```json
  {
    "error": "用户或问题不存在"   
  }
  404
  ```

## 获取提交结果

### **URL**
`GET /submission/<int:id>`

### **描述**
返回提交ID的运行结果。

**注意：判题在提交ID后自动在后台排队运行，不会阻塞。**

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "problem_id": 1,
    "status": SubmissionStatus,
    "error_code": ErrorCode,
    "log_path": "sub_data/sim_1.log",
    "waveform_path": "sub_data/wave_1.wave",
    "created_at": "time"
  }
  ```

  ```python
  class SubmissionStatus():
      QUEUED = 'queued'
      RUNNING = 'running'
      SUCCESS = 'success'
      FAILED = 'failed'
  class ErrorCode(IntEnum):
      SUCCESS                         = 0
      ERROR_COMPILE_FAIL      = 1
      ERROR_SIM_LOAD_FAIL = 2
      ERROR_SIM_RUN_FAIL  = 3
      ERROR_SIM_TIMEOUT   = 4
      ERROR_MISMATCH      = 5
      ERROR_BAT_NOT_FOUND = 6
      ERROR_UNKNOWN       = 7
  ```

- 失败
  ```json
  {
    "error": "提交记录不存在"   
  }
  404
  ```

## 获取用户历史提交记录

### **URL**
`GET /submission`

### **描述**
获取用户提交历史，返回用户的历史提交ID，status，日期

*此功能需要用户登录*

### **参数**
- 无

### **响应**
- 成功
  ```json
  [{
    "submission_id": 1,
    "created_at": "time",
    "status": SubmissionStatus
  }
  {
    ...
  }]
  ```

- 失败
  ```json
  {
    "error": "用户不存在"   
  }
  404
  ```

## 获取日志

### **URL**
`GET /submission/<int:id>/log`

### **描述**
获取指定提交的日志文件内容。

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "status": "success",
    "log_content": "log_content"
  }
  ```

- 失败
  ```json
  {
    "error": "提交记录不存在"   
  }
  404
  ```
  ```json
  {
    "error": "日志文件不存在"   
  }
  404
  ```
  ```json
  {
    "error": "无法读取日志文件"   
  }
  500
  ```

## 获取波形

### **URL**
`GET /submission/<int:id>/waveform`

### **描述**
获取指定提交的波形文件内容

### **参数**
- 无

### **响应**
- 成功
  ```json
  {
    "status": "success",
    "waveform_content": "waveform_content"
  }
  ```

- 失败
  ```json
  {
    "error": "提交记录不存在"   
  }
  404
  ```
  ```json
  {
    "error": "波形文件不存在"   
  }
  404
  ```
  ```json
  {
    "error": "无法读取波形文件"   
  }
  500
  ```

## 管理员API

### 获取所有用户

#### **URL**
`GET /admin/user`

#### **描述**
获取所有用户信息（需要管理员权限）

#### **参数**
- 无

#### **响应**
```json
[
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "is_admin": true
    },
    {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "is_admin": false
    }
]
```

### 更新用户信息

#### **URL**
`PUT /admin/user/<int:user_id>`

#### **描述**
更新指定用户的信息（需要管理员权限）

#### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "username": "string",  // 可选
    "email": "string",     // 可选
    "is_admin": boolean,   // 可选
    "password": "string"   // 可选
  }
  ```

#### **响应**
```json
{
    "status": "success"
}
```

### 删除用户

#### **URL**
`DELETE /admin/user/<int:user_id>`

#### **描述**
删除指定用户（需要管理员权限）

#### **参数**
- 无

#### **响应**
```json
{
    "status": "success"
}
```

### 获取所有题目

#### **URL**
`GET /admin/problem`

#### **描述**
获取所有题目的详细信息（需要管理员权限）

#### **参数**
- 无

#### **响应**
```json
[
    {
        "id": 1,
        "title": "string",
        "folder_path": "string",  // 题目文件夹路径
        "difficulty": "string",
        "tags": "string",
        "pre_problems": "string",  // 注意：管理员接口中的 pre_problems 是逗号分隔的字符串
        "next_problems": "string",  // 注意：管理员接口中的 pre_problems 是逗号分隔的字符串
        "description": "string",
        "code_temp": "string"
    }
]
```

### 更新题目信息

#### **URL**
`PUT /admin/problem/<int:problem_id>`

#### **描述**
更新指定题目的信息（需要管理员权限）

#### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "title": "string",       // 可选
    "folder_path": "string", // 可选，题目文件夹路径
    "difficulty": "string",  // 可选
    "tags": "string",       // 可选
    "pre_problems": "string", // 可选，前置题目ID列表，逗号分隔
    "next_problems": "string",  // 注意：管理员接口中的 pre_problems 是逗号分隔的字符串
    "description": "string", // 可选
    "code_temp": "string"   // 可选
  }
  ```

#### **响应**
```json
{
    "status": "success"
}
```

### 删除题目

#### **URL**
`DELETE /admin/problem/<int:problem_id>`

#### **描述**
删除指定题目（需要管理员权限）

#### **参数**
- 无

#### **响应**
```json
{
    "status": "success"
}
```

## 学习路径API

### 获取所有学习路径

#### **URL**
`GET //all`

#### **描述**
获取所有可用的学习路径

#### **参数**
- 无

#### **响应**
```json
[
  {
    "id": 1,
    "name": "Verilog基础入门",
    "description": "从零开始学习Verilog HDL语言基础",
    "start_problem_id": 1
  },
  {
    "id": 2,
    "name": "数字电路设计进阶",
    "description": "学习更复杂的数字电路设计技巧",
    "start_problem_id": 5
  }
]
```

### 获取单个学习路径详情

#### **URL**
`GET //<int:path_id>`

#### **描述**
获取指定ID的学习路径详情

#### **参数**
- 无

#### **响应**
- 成功
  ```json
  {
    "id": 1,
    "name": "Verilog基础入门",
    "description": "从零开始学习Verilog HDL语言基础",
    "start_problem_id": 1
  }
  ```

- 失败
  ```json
  {
    "error": "学习路径不存在"
  }
  404
  ```

### 获取学习路径的完整题目链条

#### **URL**
`GET //<int:path_id>/chain`

#### **描述**
获取学习路径的完整题目链条，从起始题目开始，根据题目的"后置"关系构建

#### **参数**
- 无

#### **响应**
- 成功
  ```json
  {
    "path_id": 1,
    "path_name": "Verilog基础入门",
    "path_description": "从零开始学习Verilog HDL语言基础",
    "problems_chain": [
      {
        "id": 1,
        "title": "Verilog基本语法",
        "difficulty": "简单",
        "tags": ["基础", "语法"]
      },
      {
        "id": 2,
        "title": "组合逻辑电路",
        "difficulty": "简单",
        "tags": ["组合逻辑"]
      },
      {
        "id": 3,
        "title": "时序逻辑电路",
        "difficulty": "中等",
        "tags": ["时序逻辑"]
      }
    ]
  }
  ```

- 失败
  ```json
  {
    "error": "学习路径不存在"
  }
  404
  ```

### 添加新的学习路径（仅管理员）

#### **URL**
`POST //add`

#### **描述**
添加新的学习路径（需要管理员权限）

#### **参数**
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "name": "string",              // 学习路径名称
    "description": "string",       // 学习路径描述
    "start_problem_id": number     // 起始题目ID
  }
  ```

#### **响应**
- 成功
  ```json
  {
    "status": "success",
    "path_id": 3
  }
  ```

- 失败
  ```json
  {
    "error": "权限不足"
  }
  403
  ```
  
  ```json
  {
    "error": "缺少必要参数"
  }
  400
  ```
  
  ```json
  {
    "error": "起始题目不存在"
  }
  404
  ```
