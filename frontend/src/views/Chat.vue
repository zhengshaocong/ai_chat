<template>
  <div class="chat-container">
    <!-- 左侧会话列表 -->
    <div class="chat-sidebar">
      <div class="sidebar-header">
        <h2>{{ currentApp.name }}</h2>
        <el-button type="primary" @click="createNewSession">新建会话</el-button>
      </div>
      <div class="session-list">
        <div
          v-for="session in chatSessions"
          :key="session.id"
          :class="['session-item', { active: currentSession?.id === session.id }]"
          @click="selectSession(session)"
        >
          <div class="session-title">{{ session.title }}</div>
          <div class="session-time">{{ formatDate(session.updated_at) }}</div>
          <el-button
            class="delete-btn"
            type="text"
            @click.stop="deleteSession(session.id)"
          >
            删除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="chat-main">
      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', message.role]"
        >
          <div class="message-content">{{ message.content }}</div>
          <div class="message-time">{{ formatDate(message.created_at) }}</div>
        </div>
      </div>
      <div class="chat-input">
        <el-input
          v-model="newMessage"
          type="textarea"
          :rows="3"
          placeholder="输入消息..."
          @keyup.enter.ctrl="sendMessage"
        />
        <div class="input-actions">
          <el-upload
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
          >
            <el-button type="primary" plain>上传文件</el-button>
          </el-upload>
          <el-button type="primary" @click="sendMessage">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Chat',
  setup() {
    const route = useRoute()
    const appId = route.params.appId
    const currentApp = ref({})
    const chatSessions = ref([])
    const currentSession = ref(null)
    const messages = ref([])
    const newMessage = ref('')
    const messagesContainer = ref(null)

    const fetchAppInfo = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/ai-apps/${appId}`)
        currentApp.value = response.data
      } catch (error) {
        console.error('Error fetching app info:', error)
      }
    }

    const fetchSessions = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/chat/sessions/${appId}`)
        chatSessions.value = response.data
      } catch (error) {
        console.error('Error fetching sessions:', error)
      }
    }

    const fetchMessages = async (sessionId) => {
      try {
        const response = await axios.get(`http://localhost:5000/api/chat/messages/${sessionId}`)
        messages.value = response.data
        await nextTick()
        scrollToBottom()
      } catch (error) {
        console.error('Error fetching messages:', error)
      }
    }

    const createNewSession = async () => {
      try {
        const response = await axios.post('http://localhost:5000/api/chat/sessions', {
          ai_app_id: appId,
          title: '新会话'
        })
        chatSessions.value.unshift(response.data)
        currentSession.value = response.data
        messages.value = []
      } catch (error) {
        console.error('Error creating session:', error)
      }
    }

    const selectSession = (session) => {
      currentSession.value = session
      fetchMessages(session.id)
    }

    const deleteSession = async (sessionId) => {
      try {
        await axios.delete(`http://localhost:5000/api/chat/sessions/${sessionId}`)
        chatSessions.value = chatSessions.value.filter(s => s.id !== sessionId)
        if (currentSession.value?.id === sessionId) {
          currentSession.value = null
          messages.value = []
        }
      } catch (error) {
        console.error('Error deleting session:', error)
      }
    }

    const sendMessage = async () => {
      if (!newMessage.value.trim() || !currentSession.value) return

      try {
        // 发送用户消息
        const userMessage = await axios.post('http://localhost:5000/api/chat/messages', {
          session_id: currentSession.value.id,
          role: 'user',
          content: newMessage.value
        })
        messages.value.push(userMessage.data)

        // 模拟AI回复
        const aiMessage = await axios.post('http://localhost:5000/api/chat/messages', {
          session_id: currentSession.value.id,
          role: 'assistant',
          content: newMessage.value // 这里应该调用实际的AI服务
        })
        messages.value.push(aiMessage.data)

        newMessage.value = ''
        await nextTick()
        scrollToBottom()
      } catch (error) {
        console.error('Error sending message:', error)
      }
    }

    const handleFileChange = (file) => {
      // 处理文件上传
      console.log('File changed:', file)
    }

    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    onMounted(() => {
      fetchAppInfo()
      fetchSessions()
    })

    return {
      currentApp,
      chatSessions,
      currentSession,
      messages,
      newMessage,
      messagesContainer,
      createNewSession,
      selectSession,
      deleteSession,
      sendMessage,
      handleFileChange,
      formatDate
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
}

.chat-sidebar {
  width: 300px;
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.sidebar-header h2 {
  margin-bottom: 15px;
}

.session-list {
  flex: 1;
  overflow-y: auto;
}

.session-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  position: relative;
}

.session-item:hover {
  background-color: #f5f7fa;
}

.session-item.active {
  background-color: #ecf5ff;
}

.session-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.session-time {
  font-size: 12px;
  color: #999;
}

.delete-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message {
  margin-bottom: 20px;
  max-width: 70%;
}

.message.user {
  margin-left: auto;
}

.message-content {
  padding: 10px 15px;
  border-radius: 10px;
  background-color: #f4f4f5;
}

.message.user .message-content {
  background-color: #ecf5ff;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #eee;
}

.input-actions {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 