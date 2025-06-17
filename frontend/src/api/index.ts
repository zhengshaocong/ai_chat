import http from '@/utils/http'
import type { Message, ChatSession, AIModule, User } from '@/types'

export const chatApi = {
  sendMessage(sessionId: string, message: string) {
    return http.post<Message>('/chat/send', { sessionId, message })
  },

  getSessions() {
    return http.get<ChatSession[]>('/chat/sessions')
  },

  createSession(moduleId: string) {
    return http.post<ChatSession>('/chat/sessions', { moduleId })
  },

  deleteSession(sessionId: string) {
    return http.delete(`/chat/sessions/${sessionId}`)
  },

  updateSessionTitle(sessionId: string, title: string) {
    return http.put(`/chat/sessions/${sessionId}/title`, { title })
  },
}

export const moduleApi = {
  getModules() {
    return http.get<AIModule[]>('/modules')
  },

  updateModuleStatus(moduleId: string, enabled: boolean) {
    return http.put(`/modules/${moduleId}/status`, { enabled })
  },
}

export const userApi = {
  login(username: string, password: string) {
    return http.post<{ token: string; user: User }>('/auth/login', {
      username,
      password,
    })
  },

  register(username: string, password: string) {
    return http.post<{ token: string; user: User }>('/auth/register', {
      username,
      password,
    })
  },

  getCurrentUser() {
    return http.get<User>('/user/current')
  },

  updateProfile(data: Partial<User>) {
    return http.put('/user/profile', data)
  },
} 