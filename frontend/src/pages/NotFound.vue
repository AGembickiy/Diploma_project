<template>
  <div class="not-found">
    <div class="error-content">
      <h1>404</h1>
      <h2>Страница не найдена</h2>
      <p>К сожалению, запрашиваемая страница не существует.</p>
      
      <div class="actions">
        <router-link to="/" class="btn btn-primary">
          Вернуться на главную
        </router-link>
        <button @click="goBack" class="btn btn-secondary">
          Назад
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.error-content h1 {
  font-size: 6rem;
  color: var(--primary-color);
  margin: 0;
  font-weight: var(--font-weight-bold);
  font-family: var(--font-family-heading);
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  letter-spacing: 0.1em;
}

.error-content h2 {
  font-size: 2rem;
  color: var(--text-color);
  margin: var(--spacing-md) 0;
  font-family: var(--font-family-heading);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.error-content p {
  font-size: 1.2rem;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
  font-family: var(--font-family-body);
  line-height: var(--line-height-relaxed);
}

.actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: var(--spacing-md) var(--spacing-xl);
  border: none;
  border-radius: var(--border-radius-md);
  text-decoration: none;
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  font-family: var(--font-family-body);
  font-weight: var(--font-weight-medium);
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: var(--white);
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.btn-secondary {
  background: linear-gradient(135deg, var(--secondary-color) 0%, var(--secondary-dark) 100%);
  color: var(--white);
  box-shadow: var(--shadow-sm);
}

.btn-secondary:hover {
  background: linear-gradient(135deg, var(--secondary-dark) 0%, var(--secondary-color) 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .error-content h1 {
    font-size: 4rem;
  }
  
  .error-content h2 {
    font-size: 1.5rem;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style> 