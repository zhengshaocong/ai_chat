<template>
  <div class="ai-app-list">
    <el-row :gutter="20">
      <el-col :span="6" v-for="app in aiApps" :key="app.id">
        <el-card class="app-card" @click="navigateToChat(app)">
          <div class="app-icon">
            <img :src="app.icon" :alt="app.name">
          </div>
          <div class="app-info">
            <h3>{{ app.name }}</h3>
            <p>{{ app.description }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'AIAppList',
  setup() {
    const router = useRouter()
    const aiApps = ref([])

    const fetchAIApps = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/ai-apps/')
        aiApps.value = response.data
      } catch (error) {
        console.error('Error fetching AI apps:', error)
      }
    }

    const navigateToChat = (app) => {
      router.push(`/chat/${app.id}`)
    }

    onMounted(() => {
      fetchAIApps()
    })

    return {
      aiApps,
      navigateToChat
    }
  }
}
</script>

<style scoped>
.ai-app-list {
  padding: 20px;
}

.app-card {
  cursor: pointer;
  transition: transform 0.3s;
  margin-bottom: 20px;
}

.app-card:hover {
  transform: translateY(-5px);
}

.app-icon {
  text-align: center;
  margin-bottom: 15px;
}

.app-icon img {
  width: 64px;
  height: 64px;
}

.app-info h3 {
  margin-bottom: 10px;
  color: #333;
}

.app-info p {
  color: #666;
  font-size: 14px;
}
</style> 