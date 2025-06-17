// 用户相关类型
export interface LoginData {
  username: string
  password: string
}

export interface UserInfo {
  id: number
  username: string
  avatar: string
  email?: string
  created_at: string
  updated_at: string
}

// 聊天相关类型
export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface Session {
  id: number
  title: string
  module_id: number
  created_at: string
  updated_at: string
  last_message?: Message
}

// 模块相关类型
export interface Module {
  id: number
  name: string
  description: string
  icon: string
  enabled: boolean
  created_at: string
  updated_at: string
}

// API 响应类型
export interface ApiResponse<T = any> {
  code: number
  message?: string
  data?: T
}

// 分页响应类型
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  moduleId: string
  createdAt: number
  updatedAt: number
}

export interface AIModule {
  id: string
  name: string
  description: string
  icon: string
  enabled: boolean
}

export interface User {
  id: string
  username: string
  avatar?: string
}

export interface ChatResponse {
  message: Message
  session: ChatSession
}

export interface ChatRequest {
  module: string
  message: string
  history?: Message[]
}

export interface LoginResponse {
  token: string
} 