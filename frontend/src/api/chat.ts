import { get, post } from '@/utils/request'
import type { Message, ChatSession, ApiResponse } from '@/types'
import type { AxiosRequestConfig } from 'axios'

export interface ChatResponse {
  message: Message
  error?: string
}

export interface ChatRequest {
  module: string
  message: string
  history?: Message[]
}

// 获取聊天会话列表
export function getChatSessions(appId: number): Promise<ApiResponse<ChatSession[]>> {
  return get<ChatSession[]>(`/api/chat/sessions/${appId}`)
}

// 创建聊天会话
export function createChatSession(appId: number, title: string): Promise<ApiResponse<ChatSession>> {
  return post<ChatSession>('/api/chat/sessions', {
    ai_app_id: appId,
    title
  })
}

// 删除聊天会话
export function deleteChatSession(sessionId: number): Promise<ApiResponse<void>> {
  const config: AxiosRequestConfig = {
    method: 'DELETE'
  }
  return post<void>(`/api/chat/sessions/${sessionId}`, {}, config)
}

// 发送聊天消息
export function sendChatMessage(data: ChatRequest): Promise<ApiResponse<ChatResponse>> {
  return post<ChatResponse>('/api/chat', data)
}

// 获取聊天历史
export function getChatHistory(module: string): Promise<ApiResponse<Message[]>> {
  return get<Message[]>(`/api/chat/history/${module}`)
}

// 清除聊天历史
export function clearChatHistory(module: string): Promise<ApiResponse<void>> {
  return post<void>(`/api/chat/clear/${module}`)
} 