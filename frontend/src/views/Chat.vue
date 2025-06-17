<template>
    <div class="chat-container">
      <el-container>
        <el-aside width="300px" class="chat-sidebar">
          <div class="sidebar-header">
            <h3>会话列表</h3>
            <el-button
              type="primary"
              :icon="Plus"
              circle
              @click="handleNewChat"
            />
          </div>
  
          <el-scrollbar class="session-list">
            <div
              v-for="session in chatStore.sessions"
              :key="session.id"
              class="session-item"
              :class="{ active: session.id === chatStore.currentSessionId }"
              @click="handleSelectSession(session)"
            >
              <div class="session-info">
                <h4>{{ session.title }}</h4>
                <p>{{ formatTime(session.updatedAt) }}</p>
              </div>
              <el-button
                type="danger"
                :icon="Delete"
                circle
                @click.stop="handleDeleteSession(session)"
              />
            </div>
          </el-scrollbar>
        </el-aside>
  
        <el-container class="chat-main">
          <template v-if="chatStore.currentSession">
            <div class="chat-messages" ref="messagesRef">
              <el-scrollbar ref="scrollbarRef">
                <message-item
                  v-for="message in chatStore.currentSession.messages"
                  :key="message.id"
                  :message="message"
                />
              </el-scrollbar>
            </div>
  
            <div class="chat-input">
              <el-input
                v-model="inputMessage"
                type="textarea"
                :rows="3"
                placeholder="输入消息..."
                resize="none"
                @keydown.enter.prevent="handleSendMessage"
              />
              <el-button
                type="primary"
                :icon="Position"
                :loading="sending"
                @click="handleSendMessage"
              >
                发送
              </el-button>
            </div>
          </template>
  
          <div v-else class="chat-empty">
            <el-empty description="选择一个会话或创建新会话" />
          </div>
        </el-container>
      </el-container>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, nextTick, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { ElMessageBox } from 'element-plus'
  import { Plus, Delete, Position } from '@element-plus/icons-vue'
  import { useChatStore } from '@/stores/chat'
  import { formatDate } from '@/utils'
  import MessageItem from '@/components/chat/MessageItem.vue'
  import type { ChatSession } from '@/types'
  
  const route = useRoute()
  const router = useRouter()
  const chatStore = useChatStore()
  
  const inputMessage = ref('')
  const sending = ref(false)
  const messagesRef = ref<HTMLElement>()
  const scrollbarRef = ref()
  
  // 监听路由参数变化
  watch(
    () => route.params.moduleId,
    async (moduleId) => {
      if (moduleId) {
        await chatStore.createSession(moduleId as string)
      }
    },
    { immediate: true }
  )
  
  // 监听消息列表变化，自动滚动到底部
  watch(
    () => chatStore.currentSession?.messages,
    async () => {
      await nextTick()
      scrollToBottom()
    },
    { deep: true }
  )
  
  onMounted(async () => {
    await chatStore.fetchSessions()
    if (chatStore.sessions.length > 0) {
      chatStore.setCurrentSession(chatStore.sessions[0].id)
    }
  })
  
  function formatTime(timestamp: number) {
    return formatDate(timestamp)
  }
  
  async function handleNewChat() {
    router.push('/modules')
  }
  
  function handleSelectSession(session: ChatSession) {
    chatStore.setCurrentSession(session.id)
  }
  
  async function handleDeleteSession(session: ChatSession) {
    try {
      await ElMessageBox.confirm('确定要删除这个会话吗？', '提示', {
        type: 'warning',
      })
      await chatStore.deleteSession(session.id)
    } catch (error) {
      if (error !== 'cancel') {
        console.error('删除会话失败:', error)
      }
    }
  }
  
  async function handleSendMessage() {
    if (!inputMessage.value.trim() || sending.value) return
  
    try {
      sending.value = true
      await chatStore.sendMessage(inputMessage.value)
      inputMessage.value = ''
    } catch (error) {
      console.error('发送消息失败:', error)
    } finally {
      sending.value = false
    }
  }
  
  function scrollToBottom() {
    if (scrollbarRef.value) {
      const scrollbar = scrollbarRef.value.wrap$
      scrollbar.scrollTop = scrollbar.scrollHeight
    }
  }
  </script>
  
  <style scoped lang="scss">
  .chat-container {
    height: 100%;
    background-color: var(--el-bg-color);
  }
  
  .chat-sidebar {
    border-right: 1px solid var(--el-border-color-light);
    background-color: var(--el-bg-color-overlay);
  
    .sidebar-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px;
      border-bottom: 1px solid var(--el-border-color-light);
  
      h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }
    }
  
    .session-list {
      height: calc(100% - 57px);
  
      .session-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        cursor: pointer;
        transition: background-color 0.3s;
  
        &:hover {
          background-color: var(--el-fill-color-light);
        }
  
        &.active {
          background-color: var(--el-color-primary-light-9);
        }
  
        .session-info {
          flex: 1;
          min-width: 0;
          margin-right: 12px;
  
          h4 {
            margin: 0 0 4px;
            font-size: 14px;
            font-weight: 500;
            @include text-ellipsis;
          }
  
          p {
            margin: 0;
            font-size: 12px;
            color: var(--el-text-color-secondary);
          }
        }
      }
    }
  }
  
  .chat-main {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .chat-messages {
    flex: 1;
    overflow: hidden;
  
    :deep(.el-scrollbar__wrap) {
      overflow-x: hidden;
    }
  }
  
  .chat-input {
    padding: 16px;
    border-top: 1px solid var(--el-border-color-light);
    background-color: var(--el-bg-color-overlay);
  
    .el-button {
      margin-top: 12px;
      width: 100%;
    }
  }
  
  .chat-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
  </style>