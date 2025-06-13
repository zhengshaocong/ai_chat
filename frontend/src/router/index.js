import { createRouter, createWebHistory } from 'vue-router'
import AIAppList from '../views/AIAppList.vue'
import Chat from '../views/Chat.vue'

const routes = [
  {
    path: '/',
    name: 'AIAppList',
    component: AIAppList
  },
  {
    path: '/chat/:appId',
    name: 'Chat',
    component: Chat
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 