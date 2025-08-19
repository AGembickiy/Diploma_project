import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const sidebarCollapsed = ref(false)
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // Управление темой
  const isDarkTheme = ref(true) // По умолчанию темная тема
  
  // Инициализация темы из localStorage
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDarkTheme.value = savedTheme === 'dark'
    } else {
      // Если нет сохраненной темы, используем системную
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      isDarkTheme.value = prefersDark
    }
    applyTheme()
  }
  
  // Применение темы к DOM
  const applyTheme = () => {
    if (isDarkTheme.value) {
      document.body.classList.remove('theme-light')
    } else {
      document.body.classList.add('theme-light')
    }
  }
  
  // Переключение темы
  const toggleTheme = () => {
    isDarkTheme.value = !isDarkTheme.value
    localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light')
    applyTheme()
  }

  // Глобальный state для модального окна входа
  const showLoginDialog = ref(false)
  const openLoginDialog = () => { 
    showLoginDialog.value = true 
  }
  const closeLoginDialog = () => { 
    showLoginDialog.value = false 
  }

  return { 
    sidebarCollapsed, 
    toggleSidebar, 
    isDarkTheme,
    toggleTheme,
    initTheme,
    showLoginDialog, 
    openLoginDialog, 
    closeLoginDialog 
  }
}) 