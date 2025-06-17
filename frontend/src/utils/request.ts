// 测试写入功能

import axios from 'axios'
import { ElMessage } from 'element-plus'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

interface ApiResponse<T = any> {
  code: number
  message?: string
  data?: T
}

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token')
    if (token) {
      // 设置请求头
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data as ApiResponse
    
    // 如果响应成功但业务状态码不为0，说明是业务错误
    if (res.code !== 0) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    
    // 如果是成功响应，显示成功消息
    if (res.message) {
      ElMessage.success(res.message)
    }
    
    // 返回响应数据
    return res
  },
  (error) => {
    // 处理HTTP错误
    const errorMessage = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(errorMessage)
    return Promise.reject(error)
  }
)

// 封装 GET 请求
export function get<T>(url: string, params?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return service.get<ApiResponse<T>>(url, { params, ...config }).then(res => res.data)
}

// 封装 POST 请求
export function post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return service.post<ApiResponse<T>>(url, data, config).then(res => res.data)
}

export default service
