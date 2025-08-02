<template>
  <Card :hover="true">
    <template #header>
      <div class="ad-info">
        <div class="ad-category">
          <img :src="getCategoryIcon(advertisement.category)" alt="" class="category-icon">
          <span class="category-text">{{ advertisement.category }}</span>
        </div>
        <span class="ad-date">{{ formatDate(advertisement.createdAt) }}</span>
      </div>
    </template>
    
    <template #actions>
      <!-- Кнопка отклика для чужих объявлений -->
      <button 
        v-if="!user.isGuest && !isOwnAdvertisement" 
        class="action-btn action-btn-response" 
        @click="handleResponse" 
        title="Откликнуться на объявление"
      >
        Отклик
      </button>
      
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
      
      <div v-if="advertisement.media" class="ad-media">
        <span v-if="advertisement.media.images" class="media-item">
          <img src="@/assets/images/icons/board_icon.png" alt="" class="media-icon">
          <span>{{ advertisement.media.images.length }}</span>
        </span>
        <span v-if="advertisement.media.video" class="media-item">
          <img src="@/assets/images/icons/feedback_icon.png" alt="" class="media-icon">
          <span>Видео</span>
        </span>
        <span v-if="advertisement.media.audio" class="media-item">
          <img src="@/assets/images/icons/user_icon.png" alt="" class="media-icon">
          <span>Аудио</span>
        </span>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import Card from '@/components/ui/Card.vue'
import type { Advertisement } from '@/types/advertisement'

interface Props {
  advertisement: Advertisement
}

interface Emits {
  (e: 'edit', advertisement: Advertisement): void
  (e: 'delete', advertisement: Advertisement): void
  (e: 'response', advertisement: Advertisement): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const user = useUserStore()

// Проверяем, является ли объявление собственным
// Пока используем простую логику - первые 2 объявления считаются "своими"
const isOwnAdvertisement = computed(() => {
  if (user.isGuest) return false
  return props.advertisement.id <= 2
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
  return icons[category] || ''
}

const formatDate = (date: Date): string => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const handleEdit = () => {
  emit('edit', props.advertisement)
}

const handleDelete = () => {
  if (confirm('Вы уверены, что хотите удалить это объявление?')) {
    emit('delete', props.advertisement)
  }
}

const handleResponse = () => {
  emit('response', props.advertisement)
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
  background: var(--success-color, #00b894);
  color: #fff;
  border-color: var(--success-color, #00b894);
}

.action-btn-response:hover {
  background: #00a085;
  border-color: #00a085;
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