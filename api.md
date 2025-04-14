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
  "msg": "需要用户名和密码"
  }
  400
  ```

  ```json
  {
  "status": "error",
  "msg": "用户名或密码错误"
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
`GET /problem`

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



