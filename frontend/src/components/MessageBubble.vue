<template>
  <div :class="['message-bubble', role]">
    <div class="avatar">
      <el-avatar :size="32" :icon="role === 'user' ? 'User' : 'Service'" />
    </div>
    <div class="content">
      <div class="message-content">
        <template v-for="(part, index) in messageParts" :key="index">
          <template v-if="typeof part === 'string'">
            {{ part }}
          </template>
          <CodeBlock
            v-else
            :code="part.code"
            :language="part.language"
          />
        </template>
      </div>
      <div class="message-footer">
        <div class="message-time">
          {{ formatTime(timestamp) }}
        </div>
        <div class="message-actions">
          <el-button
            v-if="role === 'assistant'"
            type="primary"
            link
            @click="handleCopy"
          >
            <el-icon><CopyDocument /></el-icon>
            复制
          </el-button>
          <el-button
            v-if="role === 'user'"
            type="primary"
            link
            @click="handleResend"
          >
            <el-icon><RefreshRight /></el-icon>
            重发
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { CopyDocument, RefreshRight } from '@element-plus/icons-vue'
import { copyToClipboard } from '@/utils/clipboard'
import { splitMessageWithCodeBlocks } from '@/utils/message'
import CodeBlock from './CodeBlock.vue'

const props = defineProps<{
  role: 'user' | 'assistant'
  timestamp: number
  content: string
}>()

const emit = defineEmits<{
  (e: 'resend'): void
}>()

const messageParts = computed(() => {
  return splitMessageWithCodeBlocks(props.content)
})

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString()
}

const handleCopy = async () => {
  await copyToClipboard(props.content)
}

const handleResend = () => {
  emit('resend')
}
</script>

<style lang="scss" scoped>
.message-bubble {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1rem;
  
  &.user {
    flex-direction: row-reverse;
    
    .content {
      align-items: flex-end;
      
      .message-content {
        background-color: var(--el-color-primary);
        color: white;
        border-radius: 12px 2px 12px 12px;
      }
    }
  }
  
  &.assistant {
    .content {
      align-items: flex-start;
      
      .message-content {
        background-color: var(--el-color-info-light-9);
        color: var(--el-text-color-primary);
        border-radius: 2px 12px 12px 12px;
      }
    }
  }
  
  .content {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    max-width: 70%;
    
    .message-content {
      padding: 0.8rem 1rem;
      word-break: break-word;
      white-space: pre-wrap;
    }
    
    .message-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      
      .message-time {
        font-size: 0.8rem;
        color: var(--el-text-color-secondary);
      }
      
      .message-actions {
        display: flex;
        gap: 0.5rem;
        opacity: 0;
        transition: opacity 0.3s;
      }
    }
    
    &:hover {
      .message-actions {
        opacity: 1;
      }
    }
  }
}

@include mobile {
  .message-bubble {
    .content {
      max-width: 85%;
      
      .message-actions {
        opacity: 1 !important;
      }
    }
  }
}
</style> 