import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatSession, Message } from '@/types'
import { chatApi } from '@/api'

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const currentSessionId = ref<string | null>(null)

  const currentSession = computed(() => {
    return sessions.value.find((s) => s.id === currentSessionId.value) || null
  })

  async function fetchSessions() {
    const response = await chatApi.getSessions()
    sessions.value = response
  }

  async function createSession(moduleId: string) {
    const response = await chatApi.createSession(moduleId)
    sessions.value.push(response)
    currentSessionId.value = response.id
    return response
  }

  async function deleteSession(sessionId: string) {
    await chatApi.deleteSession(sessionId)
    sessions.value = sessions.value.filter((s) => s.id !== sessionId)
    if (currentSessionId.value === sessionId) {
      currentSessionId.value = sessions.value[0]?.id || null
    }
  }

  async function updateSessionTitle(sessionId: string, title: string) {
    await chatApi.updateSessionTitle(sessionId, title)
    const session = sessions.value.find((s) => s.id === sessionId)
    if (session) {
      session.title = title
    }
  }

  async function sendMessage(content: string) {
    if (!currentSessionId.value) return
    const response = await chatApi.sendMessage(currentSessionId.value, content)
    const session = sessions.value.find((s) => s.id === currentSessionId.value)
    if (session) {
      session.messages.push(response)
      session.updatedAt = Date.now()
    }
    return response
  }

  function setCurrentSession(sessionId: string) {
    currentSessionId.value = sessionId
  }

  return {
    sessions,
    currentSessionId,
    currentSession,
    fetchSessions,
    createSession,
    deleteSession,
    updateSessionTitle,
    sendMessage,
    setCurrentSession,
  }
}) 