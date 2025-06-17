<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <h2>个人设置</h2>
            </div>
          </template>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="100px"
            @submit.prevent="handleSubmit"
          >
            <el-form-item label="头像">
              <el-upload
                class="avatar-uploader"
                action="/api/user/avatar"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <el-avatar
                  v-if="form.avatar"
                  :src="form.avatar"
                  :size="100"
                />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>

            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" />
            </el-form-item>

            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="form.newPassword"
                type="password"
                show-password
                placeholder="不修改请留空"
              />
            </el-form-item>

            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                show-password
                placeholder="不修改请留空"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" native-type="submit" :loading="loading">
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: userStore.currentUser?.username || '',
  avatar: userStore.currentUser?.avatar,
  newPassword: '',
  confirmPassword: '',
})

const validatePass = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback()
  } else {
    if (form.confirmPassword !== '') {
      if (formRef.value) {
        formRef.value.validateField('confirmPassword')
      }
    }
    callback()
  }
}

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback()
  } else if (value !== form.newPassword) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  newPassword: [
    { validator: validatePass, trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { validator: validatePass2, trigger: 'blur' },
  ],
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        const data: any = {
          username: form.username,
        }
        if (form.newPassword) {
          data.password = form.newPassword
        }
        await userStore.updateProfile(data)
        ElMessage.success('保存成功')
        form.newPassword = ''
        form.confirmPassword = ''
      } catch (error) {
        console.error('保存失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

function handleAvatarSuccess(response: any) {
  form.avatar = response.data.url
  userStore.updateProfile({ avatar: form.avatar })
  ElMessage.success('头像上传成功')
}

function beforeAvatarUpload(file: File) {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
  }
  return (isJPG || isPNG) && isLt2M
}
</script>

<style scoped lang="scss">
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-card {
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

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);

    &:hover {
      border-color: var(--el-color-primary);
    }
  }
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}
</style> 