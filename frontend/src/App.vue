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
          @click="ui.closeLoginDialog"
          aria-label="Закрыть диалог входа"
          tabindex="0"
        >
          ×
        </button>
        <h2 style="font-size: 24px; font-family: 'MedievalSharp', cursive; color: rgb(162, 155, 254); text-align: center; margin-bottom: 8px; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Вход в аккаунт</h2>
        <form @submit.prevent="handleLogin" style="display: flex; flex-direction: column; gap: 16px;">
          <label style="display: flex; flex-direction: column; gap: 4px;">
            <span style="font-size: 14px; color: #8a8a8a;">Логин</span>
            <input
              v-model="login"
              type="text"
              style="width: 100%; padding: 8px 12px; border-radius: 6px; background-color: #4a4a6a; color: rgb(162, 155, 254); border: none; outline: none; box-sizing: border-box; transition: all 0.2s ease;"
              required
              autocomplete="username"
              aria-label="Логин"
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
              @click="handleRegister"
              aria-label="Зарегистрироваться"
              tabindex="0"
            >
              Зарегистрироваться
            </button>
          </div>
        </form>
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useUserStore } from '@/stores/user'

const ui = useUiStore()
const user = useUserStore()

const login = ref('')
const password = ref('')

// Управляем overflow body при открытии модального окна
watch(() => ui.showLoginDialog, (isOpen) => {
  if (isOpen) {
    document.body.classList.add('modal-open')
  } else {
    document.body.classList.remove('modal-open')
  }
})

const handleLogin = () => {
  if (login.value && password.value) {
    user.login(login.value)
    ui.closeLoginDialog()
    login.value = ''
    password.value = ''
  }
}

const handleRegister = () => {
  if (login.value && password.value) {
    user.login(login.value) // Пока заглушка
    ui.closeLoginDialog()
    login.value = ''
    password.value = ''
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

<style scoped>
:global(body.modal-open) {
  overflow: hidden;
}
</style> 