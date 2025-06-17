<template>
  <div class="modules-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="header-card">
          <template #header>
            <div class="card-header">
              <h2>AI 模块</h2>
              <el-switch
                v-model="showEnabledOnly"
                active-text="仅显示已启用"
              />
            </div>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="module-list">
      <el-col
        v-for="module in filteredModules"
        :key="module.id"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
      >
        <el-card
          class="module-card"
          :class="{ disabled: !module.enabled }"
          @click="handleModuleClick(module)"
        >
          <template #header>
            <div class="card-header">
              <el-icon :size="24">
                <component :is="module.icon" />
              </el-icon>
              <span>{{ module.name }}</span>
              <el-switch
                v-model="module.enabled"
                @click.stop
                @change="handleStatusChange(module)"
              />
            </div>
          </template>
          <div class="card-content">
            <p>{{ module.description }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AIModule } from '@/types'
import { moduleApi } from '@/api'
import {
  ChatDotRound,
  Picture,
  Connection,
  Reading,
  VideoPlay,
  Microphone,
} from '@element-plus/icons-vue'

const router = useRouter()
const showEnabledOnly = ref(false)

const modules = ref<AIModule[]>([
  {
    id: 'chat',
    name: '通用对话',
    description: '与 AI 助手进行自然语言对话',
    icon: 'ChatDotRound',
    enabled: true,
  },
  {
    id: 'image',
    name: '文生图',
    description: '通过文字描述生成图片',
    icon: 'Picture',
    enabled: true,
  },
  {
    id: 'code',
    name: '代码助手',
    description: 'AI 编程助手，帮你写代码',
    icon: 'Connection',
    enabled: true,
  },
  {
    id: 'qa',
    name: '知识问答',
    description: '基于知识库的智能问答',
    icon: 'Reading',
    enabled: true,
  },
  {
    id: 'video',
    name: '视频生成',
    description: '通过文字描述生成视频',
    icon: 'VideoPlay',
    enabled: false,
  },
  {
    id: 'voice',
    name: '语音助手',
    description: '支持语音交互的 AI 助手',
    icon: 'Microphone',
    enabled: false,
  },
])

const filteredModules = computed(() => {
  if (showEnabledOnly.value) {
    return modules.value.filter((m) => m.enabled)
  }
  return modules.value
})

async function handleStatusChange(module: AIModule) {
  try {
    await moduleApi.updateModuleStatus(module.id, module.enabled)
    ElMessage.success(`${module.name}已${module.enabled ? '启用' : '禁用'}`)
  } catch (error) {
    module.enabled = !module.enabled
    console.error('更新模块状态失败:', error)
  }
}

function handleModuleClick(module: AIModule) {
  if (!module.enabled) {
    ElMessage.warning('该模块尚未启用')
    return
  }
  router.push(`/chat/${module.id}`)
}
</script>

<style scoped lang="scss">
.modules-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header-card {
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
}

.module-list {
  margin-top: 20px;
}

.module-card {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-5px);
  }

  &.disabled {
    opacity: 0.6;
    cursor: not-allowed;

    &:hover {
      transform: none;
    }
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 12px;

    .el-icon {
      color: var(--el-color-primary);
    }

    span {
      flex: 1;
      font-size: 16px;
      font-weight: 500;
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