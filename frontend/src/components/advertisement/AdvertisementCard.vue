<template>
  <Card :hover="true">
    <template #header>
      <div class="ad-info">
        <div class="ad-category">
          <img :src="getCategoryIcon(advertisement.category)" alt="" class="category-icon">
          <span class="category-text">{{ advertisement.category }}</span>
        </div>
        <span class="ad-date">{{ formatDate(advertisement.created_at) }}</span>
      </div>
    </template>
    
    <template #actions>
      <!-- Кнопка отклика для чужих объявлений -->
      <button 
        v-if="!user.isGuest && !isOwnAdvertisement && !hasExistingResponse" 
        class="action-btn action-btn-response" 
        @click="handleResponse" 
        title="Откликнуться на объявление"
      >
        Отклик
      </button>
      
      <!-- Кнопка отклика для отладки (временно) -->
      <button 
        v-if="user.user && isOwnAdvertisement" 
        class="action-btn action-btn-secondary" 
        disabled
        title="Это ваше объявление - отклик невозможен"
        style="opacity: 0.5; cursor: not-allowed;"
      >
        Ваше объявление
      </button>
      

      
      <!-- Сообщение о существующем отклике -->
      <span v-if="!user.isGuest && !isOwnAdvertisement && hasExistingResponse" class="existing-response-info">
        ✅ Отклик оставлен
      </span>
      
      <!-- Кнопки редактирования/удаления для своих объявлений -->
      <template v-if="!user.isGuest && isOwnAdvertisement">
        <button class="action-btn action-btn-edit" @click="handleEdit" title="Редактировать объявление">
          Редактировать
        </button>
        <button class="action-btn action-btn-danger" @click="handleDelete" title="Удалить объявление">
          Удалить
        </button>
      </template>
    </template>
    
    <div class="ad-content">
      <h3 class="ad-title">{{ advertisement.title }}</h3>
      <p class="ad-description">{{ advertisement.description }}</p>
      
      <div v-if="advertisement.image || advertisement.video || advertisement.audio" class="ad-media">
        <span v-if="advertisement.image" class="media-item">
          <img src="@/assets/images/icons/board_icon.png" alt="" class="media-icon">
          <span>Изображение</span>
        </span>
        <span v-if="advertisement.video" class="media-item">
          <img src="@/assets/images/icons/feedback_icon.png" alt="" class="media-icon">
          <span>Видео</span>
        </span>
        <span v-if="advertisement.audio" class="media-item">
          <img src="@/assets/images/icons/user_icon.png" alt="" class="media-icon">
          <span>Аудио</span>
        </span>
      </div>
      
      <div class="ad-author" v-if="advertisement.author">
        <small>Автор: {{ advertisement.author.username }}</small>
      </div>
    </div>
  </Card>
  
  <!-- Модальное окно для отклика -->
  <ResponseDialog
    v-if="isResponseModalOpen"
    :isVisible="isResponseModalOpen"
    :advertisement="advertisement"
    @close="closeResponseModal"
    @submit="handleResponseSubmit"
  />
  
  <!-- Диалог подтверждения -->
  <ConfirmationDialog
    :isVisible="isConfirmationDialogOpen"
    :message="confirmationMessage"
    @close="closeConfirmationDialog"
    :key="confirmationKey"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import Card from '@/components/ui/Card.vue'
import ResponseDialog from './ResponseDialog.vue'
import ConfirmationDialog from './ConfirmationDialog.vue'
import type { Advertisement } from '@/types/advertisement'

interface Props {
  advertisement: Advertisement
}

interface Emits {
  (e: 'edit', advertisement: Advertisement): void
  (e: 'delete', advertisement: Advertisement): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const user = useUserStore()
const isResponseModalOpen = ref(false)
const isConfirmationDialogOpen = ref(false)
const confirmationMessage = ref('')
const confirmationKey = ref(0) // Ключ для принудительного обновления ConfirmationDialog

// Проверяем, является ли объявление собственным
const isOwnAdvertisement = computed(() => {
  if (user.isGuest || !user.user || !props.advertisement.author) {
    return false
  }
  
  // Приводим ID к числам для корректного сравнения
  const authorId = Number(props.advertisement.author.id)
  const userId = Number(user.user.id)
  return authorId === userId
})

// Проверяем, есть ли уже отклик от текущего пользователя
const hasExistingResponse = computed(() => {
  if (user.isGuest || !user.user || !props.advertisement.responses) return false
  return props.advertisement.responses.some((response: any) => response.author?.id === user.user?.id)
})

const getCategoryIcon = (category: string): string => {
  const icons: Record<string, string> = {
    'Танки': '/src/assets/images/icons/tank_icon.png',
    'Хилы': '/src/assets/images/icons/healer_icon.png',
    'ДД': '/src/assets/images/icons/dd_icon.png',
    'Торговцы': '/src/assets/images/icons/merchant_icon.png',
    'Гилдмастеры': '/src/assets/images/icons/guildmaster_icon.png',
    'Квестгиверы': '/src/assets/images/icons/questgiver_icon.png',
    'Кузнецы': '/src/assets/images/icons/blacksmith_icon.png',
    'Кожевники': '/src/assets/images/icons/leatherworker_icon.png',
    'Зельевары': '/src/assets/images/icons/alchemist_icon.png',
    'Мастера заклинаний': '/src/assets/images/icons/spellmaster_icon.png'
  }
  return icons[category] || '/src/assets/images/icons/default_icon.png'
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const handleResponse = () => {
  isResponseModalOpen.value = true
}

const closeResponseModal = () => {
  isResponseModalOpen.value = false
}

const closeConfirmationDialog = () => {
  isConfirmationDialogOpen.value = false
  confirmationMessage.value = ''
  confirmationKey.value++ // Обновляем ключ для принудительного обновления
}

const handleResponseSubmit = async (responseData: { advertisementId: number; text: string }) => {
  try {
    
    const response = await fetch('http://localhost:8000/api/responses/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${user.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        advertisement_id: responseData.advertisementId,
        text: responseData.text
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      
      // Закрываем окно отклика
      isResponseModalOpen.value = false
      
      // Показываем диалог подтверждения
      confirmationMessage.value = 'Отклик успешно отправлен! Автор объявления получит уведомление на email.'
      confirmationKey.value++ // Обновляем ключ для принудительного обновления
      isConfirmationDialogOpen.value = true
      
      // Уведомление о том, что отклик отправлен, не нужно
      // emit('response', props.advertisement)
    } else {
      const errorData = await response.json()
      console.error('❌ Ошибка создания отклика:', errorData)
      
      if (response.status === 400) {
        let errorMessage = 'Ошибка создания отклика'
        
        if (errorData?.text && Array.isArray(errorData.text)) {
          errorMessage = errorData.text[0]
        } else if (errorData?.advertisement_id && Array.isArray(errorData.advertisement_id)) {
          errorMessage = errorData.advertisement_id[0]
        } else if (errorData?.non_field_errors && Array.isArray(errorData.non_field_errors)) {
          errorMessage = errorData.non_field_errors[0]
        } else if (typeof errorData === 'string') {
          errorMessage = errorData
        }
        
        alert('❌ ' + errorMessage)
      } else {
        alert('Ошибка создания отклика: ' + (errorData?.detail || 'Неизвестная ошибка'))
      }
    }
  } catch (error) {
    console.error('❌ Ошибка сети:', error)
    alert('Ошибка сети. Попробуйте позже.')
    
    // Закрываем окно отклика при ошибке
    isResponseModalOpen.value = false
  }
}

const handleEdit = () => {
  emit('edit', props.advertisement)
}

const handleDelete = () => {
  emit('delete', props.advertisement)
}
</script>

<style scoped>
.ad-info {
  flex: 1;
}

.ad-category {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.category-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.category-text {
  color: var(--primary-color, #a29bfe);
  font-family: 'MedievalSharp', cursive;
  font-size: 16px;
  font-weight: 600;
}

.ad-date {
  color: var(--text-muted, #8a8a8a);
  font-size: 14px;
  font-family: var(--font-family-body);
  display: block;
}

.ad-content {
  margin-bottom: 16px;
}

.ad-title {
  color: var(--text-primary, #fff);
  font-family: 'MedievalSharp', cursive;
  font-size: 20px;
  margin: 0 0 12px 0;
  font-weight: 600;
  line-height: 1.3;
}

.ad-description {
  color: var(--text-secondary, #b8b8b8);
  font-size: 16px;
  line-height: 1.6;
  margin: 0 0 16px 0;
  font-family: var(--font-family-body);
}

.ad-media {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.ad-author {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color, #4a4a6a);
}

.ad-author small {
  color: var(--text-muted, #8a8a8a);
  font-size: 12px;
  font-family: var(--font-family-body);
}

.media-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted, #8a8a8a);
  font-size: 14px;
  font-family: var(--font-family-body);
}

.media-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.action-btn {
  background: var(--bg-tertiary, #4a4a6a);
  border: 1px solid var(--border-color, #4a4a6a);
  color: var(--text-secondary, #b8b8b8);
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'MedievalSharp', cursive;
  font-weight: 500;
}

.action-btn:hover {
  background: var(--bg-primary, #1a1a2e);
  color: var(--text-primary, #fff);
  transform: translateY(-1px);
}

.action-btn-response {
  background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
  color: #fff;
  border-color: #00b894;
  box-shadow: 0 2px 4px rgba(0, 184, 148, 0.3);
  transition: all 0.3s ease;
}

.action-btn-response:hover {
  background: linear-gradient(135deg, #00a085 0%, #008f7a 100%);
  border-color: #00a085;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 184, 148, 0.4);
}

.action-btn-edit {
  background: var(--info-color, #74b9ff);
  color: #fff;
  border-color: var(--info-color, #74b9ff);
}

.action-btn-edit:hover {
  background: #5a9cff;
  border-color: #5a9cff;
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

.existing-response-info {
  color: var(--success-color, #00b894);
  font-size: 14px;
  font-family: var(--font-family-body);
  padding: 8px 16px;
  border-radius: 6px;
  background: linear-gradient(135deg, rgba(0, 184, 148, 0.1) 0%, rgba(0, 160, 133, 0.1) 100%);
  border: 2px solid var(--success-color, #00b894);
  display: inline-block;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 184, 148, 0.2);
}

@media (max-width: 768px) {
  .ad-title {
    font-size: 18px;
  }
  
  .ad-description {
    font-size: 14px;
  }
  
  .action-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style> 