import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
  email_verified: boolean
  date_joined: string
  login_display: string
  is_staff?: boolean
  is_superuser?: boolean
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User|null>(null)
  const token = ref<string|null>(null)
  
  const isGuest = computed(() => {
  return !user.value || !token.value
})
  const isAuthenticated = computed(() => !!user.value && !!token.value)
  const isEmailVerified = computed(() => user.value?.email_verified || false)

  function setUser(userData: User) {
    user.value = userData
  }

  function setToken(tokenValue: string) {
    token.value = tokenValue
    // Сохраняем в localStorage
    localStorage.setItem('auth_token', tokenValue)
  }

  function login(email: string, password: string) {
    // Эта функция теперь не используется, так как логика перенесена в App.vue
    // Оставлена для совместимости
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  // Загрузка профиля пользователя по токену
  async function fetchUserProfile() {
    if (!token.value) return
    
    try {
      const response = await axios.get('http://localhost:8000/api/users/profile/', {
        headers: {
          'Authorization': `Token ${token.value}`
        }
      })
      
      // Проверяем, есть ли уже данные пользователя
      if (!user.value) {
        user.value = response.data
      }
    } catch (error) {
      console.error('❌ Ошибка загрузки профиля:', error)
      // Если токен недействителен, очищаем его
      logout()
    }
  }

  // Инициализация при загрузке приложения
  async function initAuth() {
    const savedToken = localStorage.getItem('auth_token')
    if (savedToken) {
      token.value = savedToken
      // Загружаем данные пользователя по токену
      await fetchUserProfile()
    }
  }

  return { 
    user, 
    token, 
    isGuest, 
    isAuthenticated, 
    isEmailVerified,
    setUser, 
    setToken, 
    login, 
    logout, 
    initAuth,
    fetchUserProfile
  }
}) 