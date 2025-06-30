<template>
  <div class="users">
    <div class="users-header">
      <h1 class="users-title">Пользователи</h1>
      <p class="users-subtitle">Управление пользователями системы</p>
    </div>
    
    <div class="users-content">
      <div class="users-actions">
        <button class="add-user-btn">
          <span class="btn-icon">➕</span>
          Добавить пользователя
        </button>
        <div class="search-box">
          <input type="text" placeholder="Поиск пользователей..." class="search-input">
          <span class="search-icon">🔍</span>
        </div>
      </div>
      
      <div class="users-table-container">
        <table class="users-table">
          <thead>
            <tr>
              <th>Пользователь</th>
              <th>Email</th>
              <th>Роль</th>
              <th>Статус</th>
              <th>Дата регистрации</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>
                <div class="user-cell">
                  <span class="user-avatar">{{ user.avatar }}</span>
                  <span class="user-name">{{ user.name }}</span>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span class="role-badge" :class="user.role">{{ user.role }}</span>
              </td>
              <td>
                <span class="status-badge" :class="user.status">{{ user.status }}</span>
              </td>
              <td>{{ user.registered }}</td>
              <td>
                <div class="action-buttons">
                  <button class="action-btn edit" title="Редактировать">✏️</button>
                  <button class="action-btn delete" title="Удалить">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const users = ref([
  {
    id: 1,
    name: 'Иван Иванов',
    email: 'ivan@example.com',
    avatar: '👤',
    role: 'admin',
    status: 'active',
    registered: '01.01.2024'
  },
  {
    id: 2,
    name: 'Мария Петрова',
    email: 'maria@example.com',
    avatar: '👩',
    role: 'user',
    status: 'active',
    registered: '15.01.2024'
  },
  {
    id: 3,
    name: 'Алексей Сидоров',
    email: 'alex@example.com',
    avatar: '👨',
    role: 'moderator',
    status: 'inactive',
    registered: '20.01.2024'
  },
  {
    id: 4,
    name: 'Елена Козлова',
    email: 'elena@example.com',
    avatar: '👩',
    role: 'user',
    status: 'active',
    registered: '25.01.2024'
  }
])
</script>

<style scoped>
.users {
  max-width: 100%;
}

.users-header {
  margin-bottom: var(--spacing-2xl);
}

.users-title {
  color: var(--text-primary);
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-family-heading);
  margin: 0 0 var(--spacing-sm) 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.users-subtitle {
  color: var(--text-secondary);
  font-family: var(--font-family-body);
  font-size: var(--font-size-lg);
  margin: 0;
}

.users-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.users-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.add-user-btn {
  background: var(--primary-color);
  color: var(--white);
  border: none;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-family: var(--font-family-body);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  transition: all var(--duration-fast) var(--ease-in-out);
}

.add-user-btn:hover {
  background: var(--secondary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 300px;
}

.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg) var(--spacing-md) 40px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-family: var(--font-family-body);
  font-size: var(--font-size-base);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: var(--font-size-base);
}

.users-table-container {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-family-body);
}

.users-table th {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-weight: var(--font-weight-semibold);
  padding: var(--spacing-lg);
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  font-family: var(--font-family-heading);
}

.users-table td {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.users-table tr:hover {
  background: var(--bg-primary);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--white);
  font-size: var(--font-size-base);
}

.user-name {
  color: var(--text-primary);
  font-weight: var(--font-weight-medium);
}

.role-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  text-transform: capitalize;
}

.role-badge.admin {
  background: var(--primary-color);
  color: var(--white);
}

.role-badge.moderator {
  background: var(--secondary-color);
  color: var(--white);
}

.role-badge.user {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.status-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  text-transform: capitalize;
}

.status-badge.active {
  background: #10b981;
  color: var(--white);
}

.status-badge.inactive {
  background: var(--text-muted);
  color: var(--white);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  background: none;
  border: none;
  padding: var(--spacing-xs);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-base);
  transition: all var(--duration-fast) var(--ease-in-out);
}

.action-btn.edit:hover {
  background: var(--primary-color);
  color: var(--white);
}

.action-btn.delete:hover {
  background: #ef4444;
  color: var(--white);
}

/* Адаптивность */
@media (max-width: 768px) {
  .users-title {
    font-size: var(--font-size-2xl);
  }
  
  .users-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    max-width: none;
  }
  
  .users-table {
    font-size: var(--font-size-sm);
  }
  
  .users-table th,
  .users-table td {
    padding: var(--spacing-md);
  }
}
</style> 