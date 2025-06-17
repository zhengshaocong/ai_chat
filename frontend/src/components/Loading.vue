<template>
  <div class="loading-container" v-if="visible">
    <div class="loading-spinner">
      <el-icon class="is-loading" :size="24">
        <Loading />
      </el-icon>
      <span>{{ text }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Loading } from '@element-plus/icons-vue'

defineProps<{
  visible: boolean
  text?: string
}>()
</script>

<style lang="scss" scoped>
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  
  .el-icon {
    color: var(--el-color-primary);
  }
  
  span {
    color: var(--el-text-color-primary);
  }
}
</style> 