<template>
  <div class="verify-email-page">
    <div class="container">
      <div class="verify-card">
        <div class="header">
          <h1>🎮 Подтверждение Email</h1>
          <p>Активация вашего аккаунта MMORPG</p>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Проверяем токен подтверждения...</p>
        </div>

        <div v-else-if="success" class="success">
          <div class="success-icon">✅</div>
          <h2>Поздравляем!</h2>
          <p>Ваш email успешно подтвержден. Аккаунт активирован!</p>
          <p class="redirect-info">Через несколько секунд вы будете перенаправлены на главную страницу...</p>
          <div class="actions">
            <button @click="goToLogin" class="btn btn-primary">
              Войти в аккаунт
            </button>
            <button @click="goToHome" class="btn btn-secondary">
              На главную
            </button>
          </div>
        </div>

        <div v-else-if="error" class="error">
          <div class="error-icon">❌</div>
          <h2>Ошибка подтверждения</h2>
          <p>{{ errorMessage }}</p>
          <div class="actions">
            <button @click="goToRegister" class="btn btn-primary">
              Зарегистрироваться заново
            </button>
            <button @click="goToHome" class="btn btn-secondary">
              На главную
            </button>
          </div>
        </div>

        <div v-else class="form">
          <p>Введите токен подтверждения, который был отправлен на ваш email:</p>
          
          <div class="input-group">
            <label for="token">Токен подтверждения:</label>
            <input
              id="token"
              v-model="token"
              type="text"
              placeholder="Введите токен..."
              class="form-input"
              :class="{ 'error': tokenError }"
            />
            <span v-if="tokenError" class="error-text">{{ tokenError }}</span>
          </div>

          <button @click="verifyToken" class="btn btn-primary" :disabled="!token.trim()">
            Подтвердить Email
          </button>

          <div class="help-text">
            <p><strong>Не получили токен?</strong></p>
            <ul>
              <li>Проверьте папку "Спам" в вашем email</li>
              <li>Убедитесь, что указали правильный email при регистрации</li>
              <li>Токен действителен в течение 24 часов</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// Состояние
const token = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(false)
const errorMessage = ref('')
const tokenError = ref('')

// Получаем токен из URL параметров
onMounted(() => {
  const urlToken = route.query.token as string
  console.log('🔍 URL Token:', urlToken) // Логируем токен из URL
  if (urlToken) {
    token.value = urlToken
    verifyToken()
  }
})

// Функция подтверждения токена
const verifyToken = async () => {
  if (!token.value.trim()) {
    tokenError.value = 'Введите токен подтверждения'
    return
  }

  tokenError.value = ''
  loading.value = true
  error.value = false

  console.log('🔍 Отправляем токен на сервер:', token.value) // Логируем отправляемый токен

  try {
    const response = await axios.post('http://localhost:8000/api/users/verify-email/', {
      token: token.value
    })

    // Сохраняем токен авторизации
    if (response.data.token) {
      userStore.setToken(response.data.token)
      userStore.setUser(response.data.user)
    }

    success.value = true
    
    // Автоматически перенаправляем на главную страницу через 2 секунды
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (err: any) {
    error.value = true
    if (err.response?.data?.token) {
      errorMessage.value = err.response.data.token[0]
    } else if (err.response?.data?.non_field_errors) {
      errorMessage.value = err.response.data.non_field_errors[0]
    } else {
      errorMessage.value = 'Произошла ошибка при подтверждении email. Попробуйте еще раз.'
    }
  } finally {
    loading.value = false
  }
}

// Навигация
const goToLogin = () => {
  router.push('/login')
}

const goToHome = () => {
  router.push('/')
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.verify-email-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.container {
  width: 100%;
  max-width: 500px;
}

.verify-card {
  background: white;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #333;
  margin-bottom: 10px;
  font-size: 2rem;
}

.header p {
  color: #666;
  font-size: 1.1rem;
}

.loading {
  text-align: center;
  padding: 40px 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.success, .error {
  text-align: center;
  padding: 40px 0;
}

.success-icon, .error-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.success h2 {
  color: #28a745;
  margin-bottom: 15px;
}

.redirect-info {
  color: #6c757d;
  font-style: italic;
  margin-bottom: 20px;
}

.error h2 {
  color: #dc3545;
  margin-bottom: 15px;
}

.actions {
  margin-top: 30px;
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5a6fd8;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.form {
  margin-top: 20px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.form-input.error {
  border-color: #dc3545;
}

.error-text {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 5px;
  display: block;
}

.help-text {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.help-text p {
  margin-bottom: 10px;
  color: #333;
}

.help-text ul {
  margin: 0;
  padding-left: 20px;
  color: #666;
}

.help-text li {
  margin-bottom: 5px;
}

@media (max-width: 600px) {
  .verify-card {
    padding: 30px 20px;
  }
  
  .header h1 {
    font-size: 1.5rem;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style> 