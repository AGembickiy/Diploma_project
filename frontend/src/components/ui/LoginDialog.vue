<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-[1050] flex items-center justify-center bg-black/60 backdrop-blur-sm"
    @keydown.esc="handleClose"
    tabindex="0"
    aria-modal="true"
    role="dialog"
  >
    <div
      class="bg-bg-secondary rounded-xl shadow-xl p-8 w-full max-w-sm relative flex flex-col gap-6 outline-none"
      @click.stop
      ref="dialogRef"
    >
      <button
        class="absolute top-3 right-3 text-xl text-muted hover:text-primary focus:outline-none"
        @click="handleClose"
        aria-label="Закрыть диалог входа"
        tabindex="0"
      >
        ×
      </button>
      <h2 class="text-2xl font-heading text-primary text-center mb-2">Вход в аккаунт</h2>
      <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
        <label class="flex flex-col gap-1">
          <span class="text-sm text-muted">Email</span>
          <input
            v-model="email"
            type="email"
            class="input input-bordered w-full px-3 py-2 rounded bg-bg-tertiary text-primary focus:ring-2 focus:ring-primary"
            required
            autocomplete="email"
            aria-label="Email"
            tabindex="0"
          />
        </label>
        <label class="flex flex-col gap-1">
          <span class="text-sm text-muted">Пароль</span>
          <input
            v-model="password"
            type="password"
            class="input input-bordered w-full px-3 py-2 rounded bg-bg-tertiary text-primary focus:ring-2 focus:ring-primary"
            required
            autocomplete="current-password"
            aria-label="Пароль"
            tabindex="0"
          />
        </label>
        <div class="flex gap-3 mt-2">
          <button
            type="submit"
            class="flex-1 bg-primary text-white py-2 rounded hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label="Войти"
            tabindex="0"
          >
            Войти
          </button>
          <button
            type="button"
            class="flex-1 bg-secondary text-white py-2 rounded hover:bg-secondary-dark focus:outline-none focus:ring-2 focus:ring-secondary"
            @click="showRegister"
            aria-label="Зарегистрироваться"
            tabindex="0"
          >
            Зарегистрироваться
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits(['update:modelValue', 'login', 'showRegister'])

const email = ref('')
const password = ref('')
const dialogRef = ref<HTMLElement | null>(null)

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleLogin = () => {
  emit('login', { email: email.value, password: password.value })
}

const showRegister = () => {
  emit('showRegister')
}

const handleClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (target.closest('.logout-btn')) {
    return
  }
  
  if (dialogRef.value && !dialogRef.value.contains(target)) {
    handleClose()
  }
}

watch(() => props.modelValue, (val) => {
  if (val) {
    setTimeout(() => dialogRef.value?.focus(), 0)
    document.body.style.overflow = 'hidden'
    setTimeout(() => {
      window.addEventListener('click', handleClickOutside)
    }, 100)
  } else {
    document.body.style.overflow = ''
    window.removeEventListener('click', handleClickOutside)
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
  window.removeEventListener('click', handleClickOutside)
})
</script> 