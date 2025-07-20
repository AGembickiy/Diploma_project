import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const sidebarCollapsed = ref(false)
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // Глобальный state для модального окна входа
  const showLoginDialog = ref(false)
  const openLoginDialog = () => { 
    console.log('openLoginDialog called')
    showLoginDialog.value = true 
    console.log('showLoginDialog set to:', showLoginDialog.value)
  }
  const closeLoginDialog = () => { 
    console.log('closeLoginDialog called')
    showLoginDialog.value = false 
  }

  return { sidebarCollapsed, toggleSidebar, showLoginDialog, openLoginDialog, closeLoginDialog }
}) 