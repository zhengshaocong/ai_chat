<template>
  <div class="main-layout">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo">
            <img src="@/assets/icons/logo.svg" alt="Logo" />
            <span>AI Chain</span>
          </div>
          <div class="header-right">
            <el-button-group>
              <el-button :icon="Moon" @click="toggleTheme" />
              <el-button :icon="Setting" @click="showSettings = true" />
            </el-button-group>
            <el-dropdown>
              <el-avatar :size="32" :src="userStore.avatar || defaultAvatar" />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="router.push('/profile')">
                    <el-icon><User /></el-icon>
                    个人设置
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="route.path"
            class="el-menu-vertical"
            :router="true"
          >
            <el-menu-item index="/chat">
              <el-icon><ChatDotRound /></el-icon>
              <span>聊天</span>
            </el-menu-item>
            <el-menu-item index="/modules">
              <el-icon><Grid /></el-icon>
              <span>模块</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>

    <!-- 设置抽屉 -->
    <el-drawer
      v-model="showSettings"
      title="设置"
      direction="rtl"
      size="300px"
    >
      <el-form label-position="top">
        <el-form-item label="主题">
          <el-radio-group v-model="theme" @change="handleThemeChange">
            <el-radio-button label="light">浅色</el-radio-button>
            <el-radio-button label="dark">深色</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'
import {
  Moon,
  Setting,
  User,
  SwitchButton,
  ChatDotRound,
  Grid
} from '@element-plus/icons-vue'
import defaultAvatar from '@/assets/icons/avatar.svg'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const showSettings = ref(false)
const theme = ref('light')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  handleThemeChange(theme.value)
}

const handleThemeChange = (value: string) => {
  document.documentElement.setAttribute('data-theme', value)
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await userStore.logout()
    
    router.push('/login')
  } catch {
    // 用户取消操作
  }
}
</script>

<style scoped lang="scss">
.main-layout {
  height: 100vh;
  background-color: var(--el-bg-color);

  .el-container {
    height: 100%;
  }

  .el-header {
    background-color: var(--el-bg-color-overlay);
    border-bottom: 1px solid var(--el-border-color-light);
    padding: 0 20px;

    .header-content {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: space-between;

      .logo {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 20px;
        font-weight: bold;
        color: var(--el-text-color-primary);

        img {
          height: 32px;
          width: 32px;
        }
      }

      .header-right {
        display: flex;
        align-items: center;
        gap: 16px;
      }
    }
  }

  .el-aside {
    background-color: var(--el-bg-color-overlay);
    border-right: 1px solid var(--el-border-color-light);

    .el-menu {
      border-right: none;
    }
  }

  .el-main {
    padding: 20px;
    background-color: var(--el-bg-color-page);
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 