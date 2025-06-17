import request from '@/utils/request'
import type { LoginData, UserInfo, ApiResponse, LoginResponse } from '@/types'

// 登录
export function login(data: LoginData) {
  return request<ApiResponse<LoginResponse>>({
    url: '/auth/login',
    method: 'post',
    data
  })
}

// 注册
export function register(data: LoginData) {
  return request<ApiResponse>({
    url: '/auth/register',
    method: 'post',
    data
  })
}

// 退出登录
export function logout() {
  return request<ApiResponse>({
    url: '/auth/logout',
    method: 'post'
  })
}

// 获取用户信息
export function getUserInfo() {
  return request<ApiResponse<UserInfo>>({
    url: '/auth/user',
    method: 'get'
  })
}

// 更新用户信息
export function updateUserInfo(data: Partial<UserInfo>) {
  return request<ApiResponse<UserInfo>>({
    url: '/auth/user',
    method: 'put',
    data
  })
}

// 更新密码
export function updatePassword(data: { old_password: string; new_password: string }) {
  return request<ApiResponse>({
    url: '/auth/password',
    method: 'put',
    data
  })
}

// 上传头像
export function uploadAvatar(data: FormData) {
  return request<ApiResponse<{ url: string }>>({
    url: '/auth/avatar',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 