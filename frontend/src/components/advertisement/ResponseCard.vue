<template>
  <Card :variant="statusVariant" :hover="true">
    <template #header>
      <div class="response-info">
        <h3 class="response-author">{{ response.author.username }}</h3>
        <span class="response-date">{{ formatDate(response.created_at) }}</span>
        <span class="response-status" :class="statusClass">{{ getStatusText() }}</span>
      </div>
    </template>
    
    <template #actions>
      <button 
        v-if="status === 'new'"
        class="action-btn action-btn-success" 
        @click="handleAccept"
        title="Принять отклик"
      >
        Принять
      </button>
      <button 
        v-if="status === 'new'"
        class="action-btn action-btn-warning" 
        @click="handleReject"
        title="Отклонить отклик"
      >
        Отклонить
      </button>
      <button 
        class="action-btn action-btn-danger" 
        @click="handleDelete"
        title="Удалить отклик"
      >
        Удалить
      </button>
    </template>
    
    <div class="response-content">
      <p class="response-text">{{ response.text }}</p>
    </div>
    

  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
// import { useUserStore } from '@/stores/user'
import Card from '@/components/ui/Card.vue'
import type { Response } from '@/types/advertisement'

interface Props {
  response: Response
}

interface Emits {
  (e: 'delete', response: Response): void
  (e: 'accept', response: Response): void
  (e: 'reject', response: Response): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// const _user = useUserStore()

// Статус отклика из данных ответа
const status = computed(() => props.response.status)

const statusVariant = computed(() => {
  switch (status.value) {
    case 'accepted':
      return 'success'
    case 'rejected':
      return 'error'
    default:
      return 'default'
  }
})

const statusClass = computed(() => {
  switch (status.value) {
    case 'accepted':
      return 'status-accepted'
    case 'rejected':
      return 'status-rejected'
    default:
      return 'status-new'
  }
})

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusText = (): string => {
  switch (status.value) {
    case 'accepted':
      return 'Принят'
    case 'rejected':
      return 'Отклонен'
    default:
      return 'Новый'
  }
}

const handleDelete = () => {
  emit('delete', props.response)
}

const handleAccept = () => {
  emit('accept', props.response)
}

const handleReject = () => {
  emit('reject', props.response)
}
</script>

<style scoped>
.response-info {
  flex: 1;
}

.response-author {
  color: var(--primary-color, #a29bfe);
  font-family: 'MedievalSharp', cursive;
  font-size: 18px;
  margin: 0 0 4px 0;
  font-weight: 600;
}

.response-date {
  color: var(--text-muted, #8a8a8a);
  font-size: 14px;
  font-family: var(--font-family-body);
  display: block;
  margin-bottom: 4px;
}

.response-status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  font-family: var(--font-family-body);
}

.response-status.status-new {
  background: var(--info-color, #74b9ff);
  color: #fff;
}

.response-status.status-accepted {
  background: var(--success-color, #00b894);
  color: #fff;
}

.response-status.status-rejected {
  background: var(--error-color, #e17055);
  color: #fff;
}

.response-content {
  margin-bottom: 16px;
}

.response-text {
  color: var(--text-primary, #fff);
  font-size: 16px;
  line-height: 1.6;
  margin: 0;
  font-family: var(--font-family-body);
  white-space: pre-wrap;
}



.action-btn {
  background: var(--bg-tertiary, #4a4a6a);
  border: 1px solid var(--border-color, #4a4a6a);
  color: var(--text-secondary, #b8b8b8);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'MedievalSharp', cursive;
}

.action-btn:hover {
  background: var(--bg-primary, #1a1a2e);
  color: var(--text-primary, #fff);
}

.action-btn-success {
  background: var(--success-color, #00b894);
  color: #fff;
  border-color: var(--success-color, #00b894);
}

.action-btn-success:hover {
  background: #00a085;
  border-color: #00a085;
}

.action-btn-warning {
  background: var(--warning-color, #fdcb6e);
  color: #000;
  border-color: var(--warning-color, #fdcb6e);
}

.action-btn-warning:hover {
  background: #f39c12;
  border-color: #f39c12;
}

.action-btn-danger {
  background: var(--error-color, #e17055);
  color: #fff;
  border-color: var(--error-color, #e17055);
}

.action-btn-danger:hover {
  background: #d63031;
  border-color: #d63031;
}

@media (max-width: 768px) {
  .action-btn {
    padding: 8px 12px;
    font-size: 11px;
  }
}
</style> 