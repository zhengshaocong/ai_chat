<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <template #header>
            <div class="card-header">
              <h2>欢迎使用 {{ title }}</h2>
            </div>
          </template>
          <div class="card-content">
            <p>这是一个基于 AI 的智能对话系统，支持多个 AI 模块的切换和使用。</p>
            <el-button type="primary" @click="router.push('/chat')">
              开始对话
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="feature-row">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card">
          <template #header>
            <div class="card-header">
              <el-icon><ChatDotRound /></el-icon>
              <h3>智能对话</h3>
            </div>
          </template>
          <div class="card-content">
            <p>支持自然语言对话，提供智能、流畅的交互体验。</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card">
          <template #header>
            <div class="card-header">
              <el-icon><Grid /></el-icon>
              <h3>多模块支持</h3>
            </div>
          </template>
          <div class="card-content">
            <p>支持多个 AI 模块的切换，满足不同场景的需求。</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card">
          <template #header>
            <div class="card-header">
              <el-icon><Setting /></el-icon>
              <h3>个性化设置</h3>
            </div>
          </template>
          <div class="card-content">
            <p>支持个性化设置，打造专属的 AI 助手。</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ChatDotRound, Grid, Setting } from '@element-plus/icons-vue'

const router = useRouter()
const title = computed(() => import.meta.env.VITE_APP_TITLE || 'AI Chain')
</script>

<style scoped lang="scss">
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
    }
  }

  .card-content {
    text-align: center;
    padding: 20px 0;

    p {
      margin-bottom: 20px;
      color: var(--el-text-color-regular);
    }
  }
}

.feature-row {
  margin-top: 20px;
}

.feature-card {
  height: 100%;

  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;

    .el-icon {
      font-size: 20px;
      color: var(--el-color-primary);
    }

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
    }
  }

  .card-content {
    p {
      margin: 0;
      color: var(--el-text-color-regular);
    }
  }
}
</style> 