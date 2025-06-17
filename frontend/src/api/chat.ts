import { get, post } from '@/utils/request'
import type { Message } from '@/store'

export interface ChatResponse {
  message: Message
  error?: string
}

export interface ChatRequest {
  module: string
  message: string
  history?: Message[]
}

// 发送聊天消息
export function sendChatMessage(data: ChatRequest) {
  return post<ChatResponse>('/api/chat', data)
}

// 获取聊天历史
export function getChatHistory(module: string) {
  return get<Message[]>(`/api/chat/history/${module}`)
}

// 清除聊天历史
export function clearChatHistory(module: string) {
  return post<void>(`/api/chat/clear/${module}`)
} 