<template>
  <div class="message-item" :class="{ 'is-user': message.role === 'user' }">
    <div class="avatar">
      <el-avatar :size="40" :src="avatar">
        {{ message.role === 'user' ? 'U' : 'A' }}
      </el-avatar>
    </div>
    <div class="content">
      <div class="message-content" v-html="formattedContent"></div>
      <div class="message-time">{{ formatTime(message.timestamp) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import type { Message } from '@/types'
import { formatDate } from '@/utils'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { marked } from 'marked'

const props = defineProps<{
  message: Message
}>()

const userStore = useUserStore()

// 配置 marked
marked.setOptions({
  highlight: (code, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
})

const avatar = computed(() => {
  if (props.message.role === 'user') {
    return userStore.currentUser?.avatar
  }
  return undefined
})

const formattedContent = computed(() => {
  const content = props.message.content
  if (props.message.role === 'assistant') {
    // 使用 marked 处理 Markdown
    return marked(content)
  }
  return content
})

function formatTime(timestamp: number) {
  return formatDate(timestamp)
}
</script>

<style scoped lang="scss">
.message-item {
  display: flex;
  gap: 12px;
  padding: 20px;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--el-fill-color-light);
  }

  &.is-user {
    flex-direction: row-reverse;

    .content {
      align-items: flex-end;

      .message-content {
        background-color: var(--el-color-primary-light-9);
        border-radius: 12px 2px 12px 12px;
      }
    }
  }

  .avatar {
    flex-shrink: 0;
  }

  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-width: 80%;

    .message-content {
      padding: 12px 16px;
      background-color: var(--el-bg-color-overlay);
      border-radius: 2px 12px 12px 12px;
      font-size: 14px;
      line-height: 1.6;
      word-break: break-word;
      white-space: pre-wrap;

      :deep(pre) {
        margin: 8px 0;
        padding: 12px;
        background-color: var(--el-fill-color-darker);
        border-radius: 4px;
        overflow-x: auto;

        code {
          font-family: 'Fira Code', monospace;
          font-size: 13px;
        }
      }

      :deep(p) {
        margin: 8px 0;
      }

      :deep(ul), :deep(ol) {
        margin: 8px 0;
        padding-left: 20px;
      }
    }

    .message-time {
      font-size: 12px;
      color: var(--el-text-color-secondary);
    }
  }
}
</style> 