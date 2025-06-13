# AI 聊天应用

这是一个基于 Flask 和 Vue.js 的 AI 聊天应用，支持多个 AI 应用模块，每个模块都有独立的聊天会话功能。

## 功能特点

- 展示不同的 AI 应用模块
- 支持创建、删除和查看聊天会话
- 支持文本、图片和文件的上传
- 实时聊天界面
- 响应式设计

## 技术栈

### 后端
- Python 3.8+
- Flask
- SQLAlchemy
- MySQL

### 前端
- Vue 3
- Element Plus
- Vuex
- Vue Router
- Axios

## 安装和运行

### 后端设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
python init_db.py
```

4. 运行后端服务：
```bash
python run.py
```

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run serve
```

4. 构建生产版本：
```bash
npm run build
```

## 项目结构

```
.
├── app/                    # 后端应用目录
│   ├── models/            # 数据模型
│   ├── controllers/       # 控制器
│   ├── services/         # 服务层
│   └── utils/            # 工具函数
├── config/               # 配置文件
├── frontend/            # 前端应用目录
│   ├── src/             # 源代码
│   ├── public/          # 静态资源
│   └── package.json     # 依赖配置
├── requirements.txt     # Python 依赖
└── README.md           # 项目说明
```

## API 接口

### AI 应用接口
- GET /api/ai-apps/ - 获取所有 AI 应用
- GET /api/ai-apps/<id> - 获取特定 AI 应用

### 聊天接口
- GET /api/chat/sessions/<app_id> - 获取应用的聊天会话
- POST /api/chat/sessions - 创建新会话
- DELETE /api/chat/sessions/<id> - 删除会话
- GET /api/chat/messages/<session_id> - 获取会话消息
- POST /api/chat/messages - 发送新消息

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT 