<template>
  <div class="card" :class="cardClass">
    <div class="card-header">
      <div class="card-info">
        <slot name="header">
          <!-- Слот для заголовка карточки -->
        </slot>
      </div>
      <div class="card-actions">
        <slot name="actions">
          <!-- Слот для кнопок действий -->
        </slot>
      </div>
    </div>
    
    <div class="card-content">
      <slot>
        <!-- Основной контент карточки -->
      </slot>
    </div>
    
    <div class="card-footer">
      <slot name="footer">
        <!-- Слот для футера карточки -->
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'success' | 'error' | 'warning' | 'info'
  hover?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  hover: true
})

const cardClass = computed(() => ({
  'card--hover': props.hover,
  [`card--${props.variant}`]: props.variant !== 'default'
}))
</script>

<style scoped>
.card {
  background: var(--bg-secondary, #2c2c44);
  border: 2px solid var(--primary-color, #a29bfe);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
  position: relative;
  width: 100%;
  max-width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.card--hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(162, 155, 254, 0.2);
}

/* Варианты карточек */
.card--success {
  border-color: var(--success-color, #00b894);
}

.card--error {
  border-color: var(--error-color, #e17055);
}

.card--warning {
  border-color: var(--warning-color, #fdcb6e);
}

.card--info {
  border-color: var(--info-color, #74b9ff);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-info {
  flex: 1;
}

.card-actions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.card-content {
  margin-bottom: 12px;
}

.card-footer {
  border-top: 1px solid var(--border-color, #4a4a6a);
  padding-top: 8px;
}

@media (max-width: 768px) {
  .card {
    padding: 12px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 8px;
  }
  
  .card-actions {
    align-self: flex-end;
  }
}
</style> 