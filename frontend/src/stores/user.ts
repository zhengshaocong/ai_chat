import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, logout, getUserInfo } from '@/api/auth'
import type { LoginData, UserInfo, ApiResponse, LoginResponse } from '@/types'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)
  const avatar = ref<string>('')

  // 登录
  const loginAction = async (data: LoginData) => {
    try {
      const res = await login(data)
      if (res.code === 0 && res.data?.token) {
        token.value = res.data.token
        localStorage.setItem('token', res.data.token)
        await getUserInfoAction()
        return true
      }
      return false
    } catch (error) {
      return false
    }
  }

  // 获取用户信息
  const getUserInfoAction = async () => {
    try {
      const res = await getUserInfo()
      if (res.code === 0 && res.data) {
        userInfo.value = res.data
        avatar.value = res.data.avatar || ''
        return true
      }
      return false
    } catch (error) {
      return false
    }
  }

  // 退出登录
  const logoutAction = async () => {
    try {
      const res = await logout()
      if (res.code === 0) {
        token.value = ''
        userInfo.value = null
        avatar.value = ''
        console.log(12)
        localStorage.removeItem('token')
        return true
      }
      return false
    } catch (error) {
      return false
    }
  }

  return {
    token,
    userInfo,
    avatar,
    login: loginAction,
    logout: logoutAction,
    getUserInfo: getUserInfoAction
  }
}) 