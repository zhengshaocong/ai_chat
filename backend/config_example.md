# 配置说明

## 环境变量配置

在项目根目录创建 `.env` 文件，包含以下配置：

```env
# 数据库配置
DATABASE_URL=sqlite:///./ai_chain.db

# Flask 配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# 阿里云百炼平台 API 配置
BAILIAN_API_KEY=your-bailian-api-key

# 其他配置
DEBUG=True
```

## 获取百炼平台 API Key

1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 注册并登录账号
3. 在控制台获取 API Key
4. 将获取到的密钥填入 `.env` 文件

## 安装依赖

```bash
pip install requests python-dotenv
```

## 启动服务

```bash
python app.py
``` 