import { ElMessage } from 'element-plus'

export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('复制成功')
    return true
  } catch (err) {
    ElMessage.error('复制失败')
    return false
  }
} 