# AI Chain Frontend

基于 Vue 3 + TypeScript + Vite 的 AI 聊天应用前端。

## 功能特性

- 🚀 基于 Vue 3、Vite、TypeScript 等最新技术栈
- 💪 使用 Element Plus 组件库
- 📱 支持响应式布局，适配移动端
- 🎨 支持亮色/暗色主题
- 🔒 完整的用户认证系统
- 💬 支持多个 AI 模块的切换
- 📝 支持 Markdown 和代码高亮
- 🎯 使用 Pinia 进行状态管理
- 🛣️ 基于 Vue Router 的路由管理

## 开发环境要求

- Node.js >= 16.0.0
- npm >= 7.0.0

## 快速开始

1. 安装依赖：

```bash
npm install
```

2. 启动开发服务器：

```bash
npm run dev
```

3. 构建生产版本：

```bash
npm run build
```

## 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── api/            # API 接口
│   ├── assets/         # 资源文件
│   ├── components/     # 公共组件
│   ├── layouts/        # 布局组件
│   ├── router/         # 路由配置
│   ├── stores/         # 状态管理
│   ├── styles/         # 全局样式
│   ├── types/          # 类型定义
│   ├── utils/          # 工具函数
│   ├── views/          # 页面组件
│   ├── App.vue         # 根组件
│   └── main.ts         # 入口文件
├── .env                # 环境变量
├── .env.example        # 环境变量示例
├── index.html          # HTML 模板
├── package.json        # 项目配置
├── tsconfig.json       # TypeScript 配置
└── vite.config.ts      # Vite 配置
```

## 环境变量

创建 `.env` 文件并配置以下环境变量：

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_TITLE=AI Chain
```

## 开发指南

### 添加新页面

1. 在 `src/views` 目录下创建新的页面组件
2. 在 `src/router/index.ts` 中添加路由配置
3. 如果需要，在 `src/stores` 中添加状态管理

### 添加新组件

1. 在 `src/components` 目录下创建新的组件
2. 在需要使用的地方导入并使用

### 添加新 API

1. 在 `src/api` 目录下添加新的 API 接口
2. 在需要使用的地方导入并调用

## 代码规范

- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 遵循 Vue 3 组合式 API 风格
- 使用 TypeScript 类型注解

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT
