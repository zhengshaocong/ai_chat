<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <img src="@/assets/icons/logo.svg" alt="Logo" />
        <h1>{{ title }}</h1>
      </div>

      <el-tabs v-model="activeTab" class="login-tabs">
        <el-tab-pane label="登录" name="login">
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名"
                :prefix-icon="User"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="loading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            @keyup.enter="handleRegister"
          >
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名"
                :prefix-icon="User"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="确认密码"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="loading"
                @click="handleRegister"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { register } from '@/api/auth'

interface RegisterForm {
  username: string
  password: string
  confirmPassword: string
}

interface LoginForm {
  username: string
  password: string
}

const router = useRouter()
const userStore = useUserStore()

const title = ref('AI Chain')
const activeTab = ref('login')
const loading = ref(false)

const loginFormRef = ref<FormInstance>()
const loginForm = ref<LoginForm>({
  username: '',
  password: '',
})

const registerFormRef = ref<FormInstance>()
const registerForm = ref<RegisterForm>({
  username: '',
  password: '',
  confirmPassword: '',
})

const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
}

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.value.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

async function handleLogin() {
  if (!loginFormRef.value) return
  try {
    await loginFormRef.value.validate()
    loading.value = true
    const success = await userStore.login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    console.log(success)
    if (success) {
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error('登录失败，请检查用户名和密码')
    }
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  if (!registerFormRef.value) return
  try {
    await registerFormRef.value.validate()
    loading.value = true
    await register({
      username: registerForm.value.username,
      password: registerForm.value.password
    })
    activeTab.value = 'login'
    registerForm.value = {
      username: '',
      password: '',
      confirmPassword: '',
    }
  } catch (error) {
    console.error('注册失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
}

.login-box {
  width: 400px;
  padding: 40px;
  background-color: var(--el-bg-color-overlay);
  border-radius: 8px;
  box-shadow: var(--el-box-shadow-light);

  .logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 40px;

    img {
      height: 64px;
      margin-bottom: 16px;
    }

    h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  .login-tabs {
    :deep(.el-tabs__nav) {
      width: 100%;
      display: flex;

      .el-tabs__item {
        flex: 1;
        text-align: center;
      }
    }
  }

  .submit-btn {
    width: 100%;
  }
}
</style> 