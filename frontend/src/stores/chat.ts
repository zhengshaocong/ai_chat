import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatSession, Message } from '@/types'
import { getChatSessions, createChatSession, deleteChatSession, sendChatMessage } from '@/api/chat'

/**
 * 聊天状态管理 Store
 * 负责管理聊天会话的状态、消息发送和会话操作
 */
export const useChatStore = defineStore('chat', () => {
  // 聊天会话列表
  const sessions = ref<ChatSession[]>([])
  // 当前选中的会话ID
  const currentSessionId = ref<number | null>(null)

  /**
   * 计算属性：获取当前选中的会话对象
   * @returns ChatSession | null 当前会话对象，如果没有选中则返回 null
   */
  const currentSession = computed(() => {
    return sessions.value.find((s) => s.id === currentSessionId.value) || null
  })

  /**
   * 获取指定AI应用的聊天会话列表
   * @param appId AI应用ID
   */
  async function fetchSessions(appId: number) {
    const response = await getChatSessions(appId)
    if (response.code === 0 && response.data) {
      sessions.value = response.data
    }
  }

  /**
   * 创建新的聊天会话
   * @param appId AI应用ID
   * @param title 会话标题，默认为"新会话"
   * @returns Promise<ChatSession | undefined> 返回新创建的会话对象
   */
  async function createSession(appId: number, title: string = '新会话') {
    const response = await createChatSession(appId, title)
    if (response.code === 0 && response.data) {
      sessions.value.push(response.data)
      currentSessionId.value = response.data.id
      return response.data
    }
  }

  /**
   * 删除指定的聊天会话
   * @param sessionId 要删除的会话ID
   */
  async function deleteSession(sessionId: number) {
    const response = await deleteChatSession(sessionId)
    if (response.code === 0) {
      // 从会话列表中移除
      sessions.value = sessions.value.filter((s) => s.id !== sessionId)
      // 如果删除的是当前会话，则切换到第一个会话
      if (currentSessionId.value === sessionId) {
        currentSessionId.value = sessions.value[0]?.id || null
      }
    }
  }

  /**
   * 发送聊天消息
   * @param content 消息内容
   * @returns Promise<any | undefined> 返回发送结果
   */
  async function sendMessage(content: string) {
    if (!currentSessionId.value) return
    const response = await sendChatMessage({
      module: currentSessionId.value.toString(),
      message: content
    })
    if (response.code === 0 && response.data) {
      // 将新消息添加到当前会话的消息列表中
      const session = sessions.value.find((s) => s.id === currentSessionId.value)
      if (session) {
        session.messages.push(response.data.message)
        session.updated_at = new Date().toISOString()
      }
      return response.data
    }
  }

  /**
   * 设置当前选中的会话
   * @param sessionId 会话ID
   */
  function setCurrentSession(sessionId: number) {
    currentSessionId.value = sessionId
  }

  // 返回状态和方法供组件使用
  return {
    sessions,
    currentSessionId,
    currentSession,
    fetchSessions,
    createSession,
    deleteSession,
    sendMessage,
    setCurrentSession,
  }
}) 