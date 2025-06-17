import { defineStore } from 'pinia'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

export interface ChatState {
  messages: Message[]
  loading: boolean
}

export const useChatStore = defineStore('chat', {
  state: (): ChatState => ({
    messages: [],
    loading: false
  }),
  
  actions: {
    addMessage(message: Omit<Message, 'id' | 'timestamp'>) {
      this.messages.push({
        ...message,
        id: Date.now().toString(),
        timestamp: Date.now()
      })
    },
    
    clearMessages() {
      this.messages = []
    },
    
    setLoading(loading: boolean) {
      this.loading = loading
    }
  }
}) 