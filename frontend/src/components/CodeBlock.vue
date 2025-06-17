<template>
  <div class="code-block">
    <div class="code-header">
      <span class="language">{{ language }}</span>
      <el-button
        type="primary"
        link
        @click="handleCopy"
      >
        <el-icon><CopyDocument /></el-icon>
        复制代码
      </el-button>
    </div>
    <pre><code :class="language" ref="codeRef">{{ code }}</code></pre>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { CopyDocument } from '@element-plus/icons-vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { copyToClipboard } from '@/utils/clipboard'

const props = defineProps<{
  code: string
  language: string
}>()

const codeRef = ref<HTMLElement>()

onMounted(() => {
  if (codeRef.value) {
    hljs.highlightElement(codeRef.value)
  }
})

const handleCopy = async () => {
  await copyToClipboard(props.code)
}
</script>

<style lang="scss" scoped>
.code-block {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--el-bg-color-overlay);
  
  .code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    background-color: var(--el-bg-color);
    border-bottom: 1px solid var(--el-border-color-light);
    
    .language {
      font-size: 0.9rem;
      color: var(--el-text-color-secondary);
      text-transform: uppercase;
    }
  }
  
  pre {
    margin: 0;
    padding: 1rem;
    overflow-x: auto;
    
    code {
      font-family: 'Fira Code', monospace;
      font-size: 0.9rem;
      line-height: 1.5;
    }
  }
}
</style> 