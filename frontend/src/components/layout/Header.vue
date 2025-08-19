<template>
  <header class="header">
    <button class="theme-toggle theme-fixed" @click="ui.toggleTheme">
      <span v-if="ui.isDarkTheme">☀️</span>
      <span v-else>🌙</span>
    </button>
    <div class="header-container">
      <div class="logo-block">
        <img src="@/assets/images/logos/mythic_realms_logo.png" alt="Mythic Realms Logo" class="logo-img" />
        <span class="mmorpg-title">MMORPG</span>
      </div>
      <div class="header-right">
        <button class="menu-toggle" @click="toggleMobileMenu">
          <span class="menu-icon">☰</span>
        </button>
      </div>
    </div>
    <div v-if="isMobileMenuOpen" class="mobile-menu">
      <nav class="mobile-nav">
        <router-link to="/" class="mobile-nav-link" @click="closeMobileMenu">
          <span class="nav-icon">🏠</span>
          Главная
        </router-link>
        <router-link to="/about" class="mobile-nav-link" @click="closeMobileMenu">
          <span class="nav-icon">ℹ️</span>
          О проекте
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const isMobileMenuOpen = ref(false)
const ui = useUiStore()

// Инициализация темы при монтировании компонента
onMounted(() => {
  ui.initTheme()
})

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
@import '@/assets/styles/base.css';
.header {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
}
.header-container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 70px;
  position: relative;
}
.logo-block {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xl);
  z-index: 1;
}
.logo-img {
  height: 56px;
  width: auto;
  display: block;
}
.mmorpg-title {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-3xl, 2.5rem);
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  letter-spacing: 0.08em;
  text-shadow: 0 2px 4px rgba(0,0,0,0.25);
  white-space: nowrap;
  z-index: 1;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.theme-toggle,
.menu-toggle {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  font-size: var(--font-size-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
}
.theme-toggle:hover,
.menu-toggle:hover {
  color: var(--primary-color);
  background-color: var(--bg-secondary);
  transform: translateY(-1px);
}
.menu-toggle {
  display: none;
}
.mobile-menu {
  display: none;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-md);
}
.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}
.mobile-nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  transition: all var(--duration-fast) var(--ease-in-out);
  font-family: var(--font-family-body);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: var(--font-weight-medium);
}
.mobile-nav-link:hover {
  color: var(--primary-color);
  background-color: var(--bg-tertiary);
}
.mobile-nav-link.router-link-active {
  color: var(--primary-color);
  background-color: var(--bg-tertiary);
  font-weight: var(--font-weight-semibold);
}
@media (max-width: 768px) {
  .nav {
    display: none;
  }
  .menu-toggle {
    display: flex;
  }
  .mobile-menu {
    display: block;
  }
  .logo-img {
    height: 48px;
  }
}
@media (max-width: 480px) {
  .header-container {
    padding: 0 var(--spacing-md);
  }
  .logo-img {
    height: 40px;
  }
}
.theme-absolute {
  position: absolute;
  top: 0;
  height: 100%;
  display: flex;
  align-items: center;
}
.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.theme-fixed {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 1001;
}
</style> 