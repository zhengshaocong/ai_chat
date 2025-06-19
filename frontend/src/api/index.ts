import http from '@/utils/http'
import type { Message, ChatSession, AIModule, User } from '@/types'

/**
 * 聊天相关 API 接口
 * 提供聊天会话的增删改查和消息发送功能
 */
export const chatApi = {
  /**
   * 发送聊天消息
   * @param sessionId 会话ID
   * @param message 消息内容
   * @returns Promise<Message> 返回发送的消息对象
   */
  sendMessage(sessionId: string, message: string) {
    return http.post<Message>('/chat/send', { sessionId, message })
  },

  /**
   * 获取聊天会话列表
   * @returns Promise<ChatSession[]> 返回会话列表
   */
  getSessions() {
    return http.get<ChatSession[]>('/chat/sessions')
  },

  /**
   * 创建新的聊天会话
   * @param moduleId 模块ID，用于关联AI应用
   * @returns Promise<ChatSession> 返回新创建的会话对象
   */
  createSession(moduleId: string) {
    return http.post<ChatSession>('/chat/sessions', { moduleId })
  },

  /**
   * 删除聊天会话
   * @param sessionId 要删除的会话ID
   * @returns Promise<void> 删除操作结果
   */
  deleteSession(sessionId: string) {
    return http.delete(`/chat/sessions/${sessionId}`)
  },

  /**
   * 更新会话标题
   * @param sessionId 会话ID
   * @param title 新的标题
   * @returns Promise<void> 更新操作结果
   */
  updateSessionTitle(sessionId: string, title: string) {
    return http.put(`/chat/sessions/${sessionId}/title`, { title })
  },
}

/**
 * AI模块相关 API 接口
 * 提供AI模块的管理功能
 */
export const moduleApi = {
  /**
   * 获取所有AI模块列表
   * @returns Promise<AIModule[]> 返回模块列表
   */
  getModules() {
    return http.get<AIModule[]>('/modules')
  },

  /**
   * 更新模块启用状态
   * @param moduleId 模块ID
   * @param enabled 是否启用
   * @returns Promise<void> 更新操作结果
   */
  updateModuleStatus(moduleId: string, enabled: boolean) {
    return http.put(`/modules/${moduleId}/status`, { enabled })
  },
}

/**
 * 用户相关 API 接口
 * 提供用户认证和个人信息管理功能
 */
export const userApi = {
  /**
   * 用户登录
   * @param username 用户名
   * @param password 密码
   * @returns Promise<{token: string, user: User}> 返回登录令牌和用户信息
   */
  login(username: string, password: string) {
    return http.post<{ token: string; user: User }>('/auth/login', {
      username,
      password,
    })
  },

  /**
   * 用户注册
   * @param username 用户名
   * @param password 密码
   * @returns Promise<{token: string, user: User}> 返回注册令牌和用户信息
   */
  register(username: string, password: string) {
    return http.post<{ token: string; user: User }>('/auth/register', {
      username,
      password,
    })
  },

  /**
   * 获取当前登录用户信息
   * @returns Promise<User> 返回当前用户信息
   */
  getCurrentUser() {
    return http.get<User>('/user/current')
  },

  /**
   * 更新用户个人资料
   * @param data 要更新的用户数据
   * @returns Promise<void> 更新操作结果
   */
  updateProfile(data: Partial<User>) {
    return http.put('/user/profile', data)
  },
} 