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
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User|null>(null)
  const token = ref<string|null>(null)
  
  const isGuest = computed(() => {
    console.log('🔍 isGuest computed:', { user: user.value, token: token.value })
    return !user.value || !token.value
  })
  const isAuthenticated = computed(() => !!user.value && !!token.value)
  const isEmailVerified = computed(() => user.value?.email_verified || false)

  function setUser(userData: User) {
    console.log('🔧 setUser вызван с данными:', userData)
    user.value = userData
  }

  function setToken(tokenValue: string) {
    console.log('🔑 setToken вызван с токеном:', tokenValue)
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
      console.log('🔍 fetchUserProfile: загружаем профиль...')
      console.log('🔑 fetchUserProfile: токен для заголовка:', token.value?.substring(0, 10) + '...')
      const response = await axios.get('http://localhost:8000/api/users/profile/', {
        headers: {
          'Authorization': `Token ${token.value}`
        }
      })
      console.log('✅ fetchUserProfile: получены данные:', response.data)
      
      // Проверяем, есть ли уже данные пользователя
      if (!user.value) {
        user.value = response.data
        console.log('✅ fetchUserProfile: установлены данные пользователя')
      } else {
        console.log('ℹ️ fetchUserProfile: данные пользователя уже есть, не перезаписываем')
      }
    } catch (error) {
      console.error('❌ Ошибка загрузки профиля:', error)
      // Если токен недействителен, очищаем его
      logout()
    }
  }

  // Инициализация при загрузке приложения
  async function initAuth() {
    console.log('🚀 initAuth: инициализация аутентификации...')
    const savedToken = localStorage.getItem('auth_token')
    if (savedToken) {
      console.log('🔑 initAuth: найден сохраненный токен:', savedToken.substring(0, 10) + '...')
      token.value = savedToken
      // Загружаем данные пользователя по токену
      console.log('🔄 initAuth: вызываем fetchUserProfile...')
      await fetchUserProfile()
      console.log('✅ initAuth: fetchUserProfile завершен, user.value =', user.value)
    } else {
      console.log('🔑 initAuth: токен не найден')
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