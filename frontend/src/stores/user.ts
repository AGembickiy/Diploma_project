import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const username = ref<string|null>(null)
  const isGuest = computed(() => !username.value)

  function login(name: string) {
    username.value = name
  }
  function logout() {
    username.value = null
  }

  return { username, isGuest, login, logout }
}) 