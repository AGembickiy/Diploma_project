<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': isCollapsed }">
    <div class="sidebar-header">
      <button class="sidebar-toggle" @click="toggleSidebar">
        <span class="toggle-icon">{{ isCollapsed ? '→' : '←' }}</span>
      </button>
      <h3 v-if="!isCollapsed" class="sidebar-title">Меню</h3>
    </div>
    
    <nav class="sidebar-nav">
      <div class="nav-section">
        <h4 v-if="!isCollapsed" class="nav-section-title">Основное</h4>
        <ul class="nav-list">
          <li>
            <router-link to="/" class="nav-item" :title="isCollapsed ? 'Главная' : ''">
              <span class="nav-icon">🏠</span>
              <span v-if="!isCollapsed" class="nav-text">Главная</span>
            </router-link>
          </li>
          <li>
            <router-link to="/about" class="nav-item" :title="isCollapsed ? 'О проекте' : ''">
              <span class="nav-icon">ℹ️</span>
              <span v-if="!isCollapsed" class="nav-text">О проекте</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>
    
    <div class="sidebar-footer">
      <div v-if="!isCollapsed" class="user-info">
        <div class="user-avatar">👤</div>
        <div class="user-details">
          <p class="user-name">Пользователь</p>
          <p class="user-role">Гость</p>
        </div>
      </div>
      <button class="logout-btn" :title="isCollapsed ? 'Выйти' : ''">
        <span class="nav-icon">🚪</span>
        <span v-if="!isCollapsed" class="nav-text">Выйти</span>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isCollapsed = ref(false)

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.sidebar {
  background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  color: var(--text-primary);
  border-right: 1px solid var(--border-color);
  width: 280px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: var(--z-fixed);
  transition: width var(--duration-normal) var(--ease-in-out);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-lg);
}

.sidebar--collapsed {
  width: 70px;
}

.sidebar-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.sidebar-toggle {
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
  min-width: 32px;
  height: 32px;
}

.sidebar-toggle:hover {
  color: var(--primary-color);
  background: var(--bg-secondary);
  transform: translateY(-1px);
}

.sidebar-title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family-heading);
  color: var(--primary-color);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.sidebar-nav {
  flex: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
}

.nav-section {
  margin-bottom: var(--spacing-xl);
}

.nav-section-title {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family-heading);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.nav-item {
  color: var(--text-secondary);
  text-decoration: none;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  transition: all var(--duration-fast) var(--ease-in-out);
  font-family: var(--font-family-body);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
}

.nav-item:hover {
  color: var(--primary-color);
  background: var(--bg-tertiary);
  transform: translateX(4px);
}

.nav-item.router-link-active {
  color: var(--primary-color);
  background: var(--bg-tertiary);
  font-weight: var(--font-weight-semibold);
  box-shadow: var(--shadow-sm);
}

.nav-icon {
  font-size: var(--font-size-lg);
  min-width: 20px;
  text-align: center;
}

.nav-text {
  flex: 1;
}

.sidebar-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.user-avatar {
  font-size: var(--font-size-xl);
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-color);
  border-radius: var(--border-radius);
  color: var(--white);
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  margin: 0;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family-body);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  margin: 0;
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  font-family: var(--font-family-body);
}

.logout-btn {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  font-family: var(--font-family-body);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: var(--font-weight-medium);
  width: 100%;
}

.logout-btn:hover {
  color: var(--error-color);
  background: var(--bg-secondary);
  transform: translateY(-1px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--duration-normal) var(--ease-in-out);
  }
  
  .sidebar--collapsed {
    transform: translateX(0);
  }
}

/* Скроллбар для сайдбара */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: var(--border-radius);
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color);
}
</style> 