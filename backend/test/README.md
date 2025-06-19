# 千问模型测试文件

这个文件夹包含了用于测试千问大模型效果的测试文件，**直接引用app内的services**，使用测试模式避免数据库依赖。

## 设计理念

### 正式流程 vs 测试流程

**正式流程**:
```
数据库获取数据 → 传递给模型参数 → 执行获得内容
```

**测试流程**:
```
直接写历史对话 → 传递给模型参数 → 执行获得内容
```

## 文件说明

### 1. `test_qwen_service.py`
- **功能**: 完整的测试套件
- **特点**: 直接引用 `app.services.qwen_service.QwenService`
- **测试内容**:
  - 基本功能测试
  - 连续对话测试
  - 自定义历史对话测试
  - 不同模型对比测试
  - 生产模式 vs 测试模式对比

### 2. `quick_test_qwen.py`
- **功能**: 快速测试脚本
- **模式**:
  - 快速测试：单次消息测试
  - 交互式测试：实时对话测试
  - 自定义历史对话测试
  - 完整测试：运行所有测试

## 核心特性

### 测试模式支持
在 `app/services/qwen_service.py` 中添加了 `test_mode` 参数：

```python
# 测试模式：不保存到数据库
service = QwenService(test_mode=True)
result = service.chat_with_qwen("你好")

# 生产模式：保存到数据库
service = QwenService(test_mode=False)
result = service.chat_with_qwen("你好", session_id=1)
```

### 参数传递方式
```python
# 直接传递历史对话（测试模式）
history = [
    {"role": "user", "content": "用户消息1"},
    {"role": "assistant", "content": "AI回复1"},
    {"role": "user", "content": "用户消息2"},
    {"role": "assistant", "content": "AI回复2"}
]
result = service.chat_with_qwen("新消息", history=history)
```

## 使用方法

### 1. 环境配置
在项目根目录创建 `.env` 文件：
```env
BAILIAN_API_KEY=你的百炼平台API密钥
```

### 2. 运行测试

#### 快速测试
```bash
cd test
python quick_test_qwen.py
```

#### 完整测试
```bash
cd test
python test_qwen_service.py
```

#### 直接使用服务类
```python
from app.services.qwen_service import QwenService

# 创建测试服务
service = QwenService(test_mode=True)

# 单条消息测试
result = service.chat_with_qwen("你好")

# 连续对话测试
history = []
messages = ["你好", "请介绍一下Python", "谢谢"]

for message in messages:
    result = service.chat_with_qwen(message, history=history)
    if result["success"]:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": result['message']})

# 自定义历史对话测试
custom_history = [
    {"role": "user", "content": "什么是AI？"},
    {"role": "assistant", "content": "AI是人工智能的缩写..."}
]
result = service.chat_with_qwen("机器学习是什么？", history=custom_history)
```

## 测试结果格式

### 测试模式结果
```python
{
    "success": True,
    "message": "AI回复内容",
    "model_used": "qwen-turbo",
    "mode": "test",
    "timestamp": "2024-01-01T12:00:00",
    "request_info": {
        "model": "qwen-turbo",
        "message_count": 3,
        "temperature": 0.7,
        "max_tokens": 1500
    }
}
```

### 生产模式结果
```python
{
    "success": True,
    "message": "AI回复内容",
    "model_used": "qwen-turbo",
    "user_message_id": 123,
    "ai_message_id": 124,
    "mode": "production"
}
```

## 优势

1. **代码复用**: 直接使用app内的服务类，无需重复代码
2. **测试隔离**: 测试模式不依赖数据库，可以独立运行
3. **参数灵活**: 可以自由传入历史对话，模拟各种场景
4. **模式对比**: 可以对比测试模式和生产模式的区别
5. **易于维护**: 服务类修改后，测试自动使用最新版本

## 注意事项

1. **API密钥**: 确保设置了正确的 `BAILIAN_API_KEY` 环境变量
2. **网络连接**: 需要能够访问百炼平台API
3. **调用限制**: 注意API调用频率限制
4. **测试模式**: 测试模式下不会保存数据到数据库

## 扩展测试

你可以基于现有的服务类创建更多测试场景：

```python
# 自定义测试场景
def my_custom_test():
    service = QwenService(test_mode=True)
    
    # 模拟特定场景的历史对话
    scenario_history = [
        {"role": "user", "content": "你的场景消息"},
        {"role": "assistant", "content": "预期的AI回复"}
    ]
    
    result = service.chat_with_qwen("测试消息", history=scenario_history)
    print(result)
``` 