<template>
  <router-view />
    <teleport to="body">
    <div
      v-if="ui.showLoginDialog"
      style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 99999; display: flex; align-items: center; justify-content: center; background-color: rgba(0,0,0,0.8);"
      @click="ui.closeLoginDialog"
    >
      <div
        style="background-color: #2c2c44; border-radius: 12px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8); padding: 32px; width: 100%; max-width: 384px; position: relative; display: flex; flex-direction: column; gap: 24px; outline: none;"
        @click.stop
      >
        <button
          style="position: absolute; top: 12px; right: 12px; font-size: 24px; color: #8a8a8a; background: none; border: none; cursor: pointer;"
          @click="closeAll"
          aria-label="Закрыть диалог входа"
          tabindex="0"
        >
          ×
        </button>
        <template v-if="dialogState === 'login'">
          <h2 style="font-size: 24px; font-family: 'MedievalSharp', cursive; color: rgb(162, 155, 254); text-align: center; margin-bottom: 8px; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Вход в аккаунт</h2>
          <form @submit.prevent="handleLogin" style="display: flex; flex-direction: column; gap: 16px;">
            <label style="display: flex; flex-direction: column; gap: 4px;">
              <span style="font-size: 14px; color: #8a8a8a;">Email</span>
              <input
                v-model="login"
                type="email"
                style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
                required
                autocomplete="email"
                aria-label="Email"
                tabindex="0"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </label>
            <label style="display: flex; flex-direction: column; gap: 4px;">
              <span style="font-size: 14px; color: #8a8a8a;">Пароль</span>
              <input
                v-model="password"
                type="password"
                style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
                required
                autocomplete="current-password"
                aria-label="Пароль"
                tabindex="0"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </label>
            <div style="display: flex; gap: 12px; margin-top: 8px;">
              <button
                type="submit"
                style="flex: 1; background-color: rgb(142, 135, 234); color: rgb(255, 255, 255); padding: 8px; border-radius: 6px; border: none; cursor: pointer; font-family: 'MedievalSharp', cursive; text-shadow: 0 1px 2px rgba(0,0,0,0.3);"
                aria-label="Войти"
                tabindex="0"
              >
                Войти
              </button>
              <button
                type="button"
                style="flex: 1; background-color: rgb(230, 157, 140); color: rgb(255, 255, 255); padding: 8px; border-radius: 6px; border: none; cursor: pointer; font-family: 'MedievalSharp', cursive; text-shadow: 0 1px 2px rgba(0,0,0,0.3);"
                @click="switchToRegister"
                aria-label="Зарегистрироваться"
                tabindex="0"
              >
                Зарегистрироваться
              </button>
            </div>
          </form>
        </template>
        <template v-else-if="dialogState === 'register'">
          <h2 style="font-size: 24px; font-family: 'MedievalSharp', cursive; color: rgb(162, 155, 254); text-align: center; margin-bottom: 8px; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Регистрация</h2>
          <form @submit.prevent="handleRegisterSubmit" style="display: flex; flex-direction: column; gap: 16px;">
            <label style="display: flex; flex-direction: column; gap: 4px;">
              <span style="font-size: 14px; color: #8a8a8a;">Имя пользователя</span>
              <input
                v-model="regLogin"
                type="text"
                style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
                required
                autocomplete="username"
                aria-label="Имя пользователя"
                tabindex="0"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </label>
            <label style="display: flex; flex-direction: column; gap: 4px;">
              <span style="font-size: 14px; color: #8a8a8a;">Email</span>
              <input
                v-model="regEmail"
                type="email"
                style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
                required
                autocomplete="email"
                aria-label="Email"
                tabindex="0"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </label>
            <label style="display: flex; flex-direction: column; gap: 4px;">
              <span style="font-size: 14px; color: #8a8a8a;">Пароль</span>
              <input
                v-model="regPassword"
                type="password"
                style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
                required
                autocomplete="new-password"
                aria-label="Пароль"
                tabindex="0"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </label>
            <label style="display: flex; flex-direction: column; gap: 4px;">
              <span style="font-size: 14px; color: #8a8a8a;">Повторите пароль</span>
              <input
                v-model="regPasswordRepeat"
                type="password"
                style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
                required
                autocomplete="new-password"
                aria-label="Повторите пароль"
                tabindex="0"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </label>
            <button
              type="submit"
              style="background-color: rgb(142, 135, 234); color: rgb(255, 255, 255); padding: 8px; border-radius: 6px; border: none; cursor: pointer; font-family: 'MedievalSharp', cursive; text-shadow: 0 1px 2px rgba(0,0,0,0.3); margin-top: 8px;"
              aria-label="Зарегистрироваться"
              tabindex="0"
            >
              Зарегистрироваться
            </button>
            <button
              type="button"
              style="background: none; color: #a29bfe; text-decoration: underline; border: none; cursor: pointer; margin-top: 0; font-size: 14px;"
              @click="switchToLogin"
            >
              Уже есть аккаунт? Войти
            </button>
          </form>
        </template>
        <template v-else-if="dialogState === 'register-success'">
          <div style="text-align: center; color: #a29bfe; font-size: 18px; font-family: 'MedievalSharp', cursive;">
            <div style="font-size: 48px; margin-bottom: 16px;">✅</div>
            <div style="margin-bottom: 16px;">Регистрация успешна!</div>
            <div style="font-size: 14px; color: #8a8a8a; line-height: 1.5;">
              Мы отправили письмо с подтверждением на ваш email.<br>
              Пожалуйста, проверьте вашу почту и перейдите по ссылке для активации аккаунта.
            </div>
          </div>
          <button
            type="button"
            style="margin: 24px auto 0 auto; display: block; background-color: rgb(142, 135, 234); color: #fff; padding: 8px 24px; border-radius: 6px; border: none; cursor: pointer; font-family: 'MedievalSharp', cursive; text-shadow: 0 1px 2px rgba(0,0,0,0.3);"
            @click="closeAll"
          >
            Понятно
          </button>
        </template>
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useUserStore } from '@/stores/user'

const ui = useUiStore()
const user = useUserStore()

// Инициализация темы и аутентификации при загрузке приложения
onMounted(() => {
  ui.initTheme()
  user.initAuth()
})

const login = ref('')
const password = ref('')

// Registration form state
const regLogin = ref('')
const regEmail = ref('')
const regPassword = ref('')
const regPasswordRepeat = ref('')

const dialogState = ref<'login' | 'register' | 'register-success'>('login')

const switchToRegister = () => {
  dialogState.value = 'register'
  regLogin.value = ''
  regEmail.value = ''
  regPassword.value = ''
  regPasswordRepeat.value = ''
}
const switchToLogin = () => {
  dialogState.value = 'login'
}
const closeAll = () => {
  dialogState.value = 'login'
  ui.closeLoginDialog()
}

// Управляем overflow body при открытии модального окна (только для логина)
watch(() => ui.showLoginDialog, (isOpen) => {
  if (isOpen) {
    document.body.classList.add('modal-open')
  } else {
    document.body.classList.remove('modal-open')
  }
})

const handleLogin = async () => {
  if (!login.value || !password.value) {
    alert('Введите email и пароль!')
    return
  }
  
  try {
    const response = await fetch('http://localhost:8000/api/users/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: login.value,
        password: password.value
      })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      // Сохраняем токен и данные пользователя
      if (data.token) {
        user.setToken(data.token)
        user.setUser(data.user)
        // Не нужно загружать профиль повторно, данные уже есть в data.user
      }
      closeAll()
      login.value = ''
      password.value = ''
    } else {
      // Показываем ошибки
      let errorMessage = 'Ошибка входа:'
      if (data.email) {
        errorMessage += `\n- ${data.email[0]}`
      }
      if (data.password) {
        errorMessage += `\n- ${data.password[0]}`
      }
      if (data.non_field_errors) {
        errorMessage += `\n- ${data.non_field_errors[0]}`
      }
      alert(errorMessage)
    }
  } catch (error) {
    alert('Ошибка сети. Попробуйте еще раз.')
  }
}

const handleRegisterSubmit = async () => {
  if (!regEmail.value || !regPassword.value || !regPasswordRepeat.value) {
    alert('Заполните все обязательные поля!')
    return
  }
  
  if (regPassword.value !== regPasswordRepeat.value) {
    alert('Пароли не совпадают!')
    return
  }
  
  if (regPassword.value.length < 8) {
    alert('Пароль должен содержать минимум 8 символов!')
    return
  }
  
  try {
    const response = await fetch('http://localhost:8000/api/users/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: regLogin.value || undefined,
        email: regEmail.value,
        password: regPassword.value,
        password_confirm: regPasswordRepeat.value
      })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      dialogState.value = 'register-success'
      // Очищаем форму
      regLogin.value = ''
      regEmail.value = ''
      regPassword.value = ''
      regPasswordRepeat.value = ''
    } else {
      // Показываем ошибки
      let errorMessage = 'Ошибка при регистрации:'
      if (data.email) {
        errorMessage += `\n- ${data.email[0]}`
      }
      if (data.password) {
        errorMessage += `\n- ${data.password[0]}`
      }
      if (data.non_field_errors) {
        errorMessage += `\n- ${data.non_field_errors[0]}`
      }
      alert(errorMessage)
    }
  } catch (error) {
    alert('Ошибка сети. Попробуйте еще раз.')
  }
}

const handleInputFocus = (e: Event) => {
  const target = e.target as HTMLInputElement
  target.style.boxShadow = '0 0 0 2px rgb(172, 165, 254)'
}

const handleInputBlur = (e: Event) => {
  const target = e.target as HTMLInputElement
  target.style.boxShadow = 'none'
}
</script>

<!-- Стили для компонента App -->
<style scoped>
</style> 