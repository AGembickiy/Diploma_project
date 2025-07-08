<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': isCollapsed }">
    <div class="sidebar-header">
      <button class="sidebar-toggle" @click="toggleSidebar">
        <img :src="isCollapsed ? leftArrowPng : rightArrowPng" alt="toggle" class="toggle-arrow" />
      </button>
      <h3 v-if="!isCollapsed" class="sidebar-title">Меню</h3>
    </div>
    
    <nav class="sidebar-nav">
      <div class="nav-section">
        <ul class="nav-list">
          <li>
            <router-link to="/" class="nav-item" :title="isCollapsed ? 'Главная' : ''" :class="{ 'centered': isCollapsed }">
              <img :src="homepageIcon" alt="Главная" class="nav-icon" />
              <span v-if="!isCollapsed" class="nav-text">Главная</span>
            </router-link>
          </li>
          <li>
            <router-link to="/board" class="nav-item" :title="isCollapsed ? 'Доска объявлений' : ''" :class="{ 'centered': isCollapsed }">
              <img :src="boardIcon" alt="Доска объявлений" class="nav-icon" />
              <span v-if="!isCollapsed" class="nav-text">Доска объявлений</span>
            </router-link>
          </li>
          <li>
            <router-link to="/responses" class="nav-item" :title="isCollapsed ? 'Отклики' : ''" :class="{ 'centered': isCollapsed }">
              <img :src="feedbackIcon" alt="Отклики" class="nav-icon" />
              <span v-if="!isCollapsed" class="nav-text">Отклики</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>
    
    <div class="sidebar-footer">
      <div class="user-info" :class="{ 'centered': isCollapsed }">
        <div class="user-avatar"><img :src="userIcon" alt="Пользователь" class="user-avatar-img" /></div>
        <div v-if="!isCollapsed" class="user-details">
          <p class="user-name">{{ user.isGuest ? 'Гость' : user.username }}</p>
          <p class="user-role">{{ user.isGuest ? 'Гость' : 'Пользователь' }}</p>
        </div>
      </div>
      <button class="logout-btn" :title="isCollapsed ? (user.isGuest ? 'Войти' : 'Выйти') : ''" @click="handleAuthClick">
        <img :src="openDoorIcon" :alt="user.isGuest ? 'Войти' : 'Выйти'" class="nav-icon" />
        <span v-if="!isCollapsed" class="nav-text">{{ user.isGuest ? 'Войти' : 'Выйти' }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useUserStore } from '@/stores/user'
import homepageIcon from '@/assets/images/icons/homepage_icon.png'
import boardIcon from '@/assets/images/icons/board_icon.png'
import feedbackIcon from '@/assets/images/icons/feedback_icon.png'
import leftArrowPng from '@/assets/images/icons/left_arrow.png'
import rightArrowPng from '@/assets/images/icons/right_arrow.png'
import userIcon from '@/assets/images/icons/user_icon.png'
import openDoorIcon from '@/assets/images/icons/open_door.png'

const ui = useUiStore()
const isCollapsed = computed(() => ui.sidebarCollapsed)
const toggleSidebar = ui.toggleSidebar

const user = useUserStore()

function handleAuthClick() {
  if (user.isGuest) {
    user.login('DemoUser')
  } else {
    user.logout()
  }
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
  justify-content: space-between;
  box-shadow: var(--shadow-lg);
}

.sidebar--collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 10px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.sidebar-toggle {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 10px;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  font-size: var(--font-size-lg);
  display: flex;
  align-items: center;
  justify-content: center;
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
  padding: 10px;
  overflow-y: visible;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.nav-section {
  margin-bottom: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.nav-list {
  list-style: none;
  padding: 0 10px;
  margin: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.nav-item {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 10px;
  transition: all var(--duration-fast) var(--ease-in-out);
  font-family: var(--font-family-body);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
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
  font-size: 2rem;
  width: 32px;
  height: 32px;
  text-align: center;
  object-fit: contain;
  display: block;
}

.nav-text {
  flex: 1;
  font-size: 1.15rem;
}

.sidebar-footer {
  padding: 10px;
  border-top: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 10px;
  background: var(--bg-tertiary);
  border: none;
}

.user-avatar {
  font-size: var(--font-size-xl);
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-color);
  color: var(--white);
}

.user-avatar-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  display: block;
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
  border: none;
  color: var(--text-secondary);
  padding: 10px;
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

.toggle-arrow {
  width: 36px;
  height: 36px;
  display: block;
  object-fit: contain;
  transition: transform var(--duration-fast) var(--ease-in-out);
}

/* Центрирование для .nav-item и .user-info при isCollapsed */
.centered {
  justify-content: center !important;
}

.user-info.centered {
  flex-direction: column;
  align-items: center;
}
</style> 