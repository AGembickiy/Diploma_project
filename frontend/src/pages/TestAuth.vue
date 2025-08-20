<template>
  <div class="test-auth">
    <h1>Тест аутентификации</h1>
    
    <div class="auth-section">
      <h2>Текущий статус</h2>
      <p>Токен: {{ token || 'Не установлен' }}</p>
      <p>Пользователь: {{ user ? user.username : 'Не авторизован' }}</p>
      <p>Email: {{ user ? user.email : 'Не авторизован' }}</p>
    </div>
    
    <div class="auth-section">
      <h2>Установить тестовый токен</h2>
      <button @click="setTestToken" class="btn btn-primary">
        Установить тестовый токен
      </button>
      <button @click="clearToken" class="btn btn-danger">
        Очистить токен
      </button>
    </div>
    
    <div class="auth-section">
      <h2>Тест API</h2>
      <button @click="testResponsesAPI" class="btn btn-success">
        Тест API откликов
      </button>
      <button @click="testAdvertisementsAPI" class="btn btn-success">
        Тест API объявлений
      </button>
      
      <div v-if="apiResult" class="api-result">
        <h3>Результат API:</h3>
        <pre>{{ JSON.stringify(apiResult, null, 2) }}</pre>
      </div>
    </div>
    
    <div class="auth-section">
      <h2>Навигация</h2>
      <router-link to="/responses" class="btn btn-info">
        Перейти к откликам
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { ResponsesService } from '@/services/responses'

const userStore = useUserStore()

const token = computed(() => userStore.token)
const user = computed(() => userStore.user)
const apiResult = ref<any>(null)

const setTestToken = () => {
  const testToken = '780abe938000e4d763c7a763ecbe85cd1f279d67'
  userStore.setToken(testToken)
  userStore.fetchUserProfile()
}

const clearToken = () => {
  userStore.logout()
  apiResult.value = null
}

const testResponsesAPI = async () => {
  try {
    const result = await ResponsesService.getMyAdvertisementResponses()
    apiResult.value = result
  } catch (error: any) {
    apiResult.value = { error: error.message || 'Неизвестная ошибка' }
  }
}

const testAdvertisementsAPI = async () => {
  try {
    const result = await ResponsesService.getMyAdvertisements()
    apiResult.value = result
  } catch (error: any) {
    apiResult.value = { error: error.message || 'Неизвестная ошибка' }
  }
}
</script>

<style scoped>
.test-auth {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.auth-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  margin: 0.25rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.api-result {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.api-result pre {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
