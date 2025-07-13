<template>
  <div class="announcement-card" :class="{ 'announcement-card--inactive': !announcement.isActive }">
    <!-- Заголовок карточки -->
    <div class="announcement-card__header">
      <div class="announcement-card__category">
        <img 
          :src="categoryInfo.icon" 
          :alt="categoryInfo.label"
          class="announcement-card__category-icon"
        />
        <span class="announcement-card__category-label">{{ categoryInfo.label }}</span>
      </div>
      <div class="announcement-card__meta">
        <span class="announcement-card__author">{{ announcement.author }}</span>
        <span class="announcement-card__date">{{ formattedDate }}</span>
      </div>
    </div>

    <!-- Заголовок объявления -->
    <h3 class="announcement-card__title">{{ announcement.title }}</h3>

    <!-- Контент объявления -->
    <div class="announcement-card__content">
      <!-- Текстовый контент -->
      <div class="announcement-card__text" v-html="formattedContent"></div>

      <!-- Изображения -->
      <div v-if="announcement.images && announcement.images.length > 0" class="announcement-card__images">
        <div class="announcement-card__images-grid">
          <div 
            v-for="(image, index) in announcement.images" 
            :key="index"
            class="announcement-card__image-wrapper"
            @click="openImageModal(image)"
          >
            <img 
              :src="image" 
              :alt="`Изображение ${index + 1}`"
              class="announcement-card__image"
              loading="lazy"
            />
          </div>
        </div>
      </div>

      <!-- Видео -->
      <div v-if="announcement.videos && announcement.videos.length > 0" class="announcement-card__videos">
        <div 
          v-for="(video, index) in announcement.videos" 
          :key="index"
          class="announcement-card__video-wrapper"
        >
          <video 
            :src="video" 
            controls
            class="announcement-card__video"
            preload="metadata"
          >
            Ваш браузер не поддерживает видео.
          </video>
        </div>
      </div>
    </div>

    <!-- Футер карточки -->
    <div class="announcement-card__footer">
      <div class="announcement-card__status">
        <span 
          class="announcement-card__status-badge"
          :class="{ 'announcement-card__status-badge--active': announcement.isActive }"
        >
          {{ announcement.isActive ? 'Активно' : 'Неактивно' }}
        </span>
      </div>
      <div class="announcement-card__actions">
        <button 
          v-if="announcement.updatedAt"
          class="announcement-card__action-btn"
          @click="showUpdateInfo"
        >
          Обновлено {{ formatUpdateDate }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Announcement } from '@/types/announcement'
import { ANNOUNCEMENT_CATEGORIES } from '@/types/announcement'

interface Props {
  announcement: Announcement
}

const props = defineProps<Props>()

// Получаем информацию о категории
const categoryInfo = computed(() => {
  return ANNOUNCEMENT_CATEGORIES.find(cat => cat.value === props.announcement.category)!
})

// Форматируем дату создания
const formattedDate = computed(() => {
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(props.announcement.createdAt)
})

// Форматируем дату обновления
const formatUpdateDate = computed(() => {
  if (!props.announcement.updatedAt) return ''
  
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(props.announcement.updatedAt)
})

// Форматируем контент с поддержкой HTML
const formattedContent = computed(() => {
  // Простое форматирование текста (можно расширить)
  return props.announcement.content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
})

// Методы
const openImageModal = (imageUrl: string) => {
  // Здесь можно добавить модальное окно для просмотра изображений
  window.open(imageUrl, '_blank')
}

const showUpdateInfo = () => {
  // Здесь можно добавить показ информации об обновлении
  console.log('Обновлено:', props.announcement.updatedAt)
}
</script>

<style scoped>
.announcement-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  transition: all var(--duration-normal) var(--ease-in-out);
  box-shadow: var(--shadow);
}

.announcement-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.announcement-card--inactive {
  opacity: 0.7;
  filter: grayscale(0.3);
}

/* Заголовок карточки */
.announcement-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.announcement-card__category {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  border-left: 4px solid v-bind('categoryInfo.color');
}

.announcement-card__category-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.announcement-card__category-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.announcement-card__meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-xs);
}

.announcement-card__author {
  font-size: var(--font-size-sm);
  color: var(--primary-color);
  font-weight: var(--font-weight-medium);
}

.announcement-card__date {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

/* Заголовок объявления */
.announcement-card__title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  line-height: var(--line-height-tight);
}

/* Контент */
.announcement-card__content {
  margin-bottom: var(--spacing-lg);
}

.announcement-card__text {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.announcement-card__text :deep(strong) {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.announcement-card__text :deep(em) {
  font-style: italic;
  color: var(--primary-color);
}

/* Изображения */
.announcement-card__images {
  margin-bottom: var(--spacing-md);
}

.announcement-card__images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-sm);
}

.announcement-card__image-wrapper {
  cursor: pointer;
  border-radius: var(--border-radius);
  overflow: hidden;
  transition: transform var(--duration-fast) var(--ease-in-out);
}

.announcement-card__image-wrapper:hover {
  transform: scale(1.05);
}

.announcement-card__image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}

/* Видео */
.announcement-card__videos {
  margin-bottom: var(--spacing-md);
}

.announcement-card__video-wrapper {
  margin-bottom: var(--spacing-sm);
}

.announcement-card__video {
  width: 100%;
  max-height: 300px;
  border-radius: var(--border-radius);
  background: var(--bg-tertiary);
}

/* Футер */
.announcement-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-light);
}

.announcement-card__status-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  background: var(--error-color);
  color: var(--white);
}

.announcement-card__status-badge--active {
  background: var(--success-color);
}

.announcement-card__action-btn {
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
}

.announcement-card__action-btn:hover {
  background: var(--primary-color);
  color: var(--white);
  border-color: var(--primary-color);
}

/* Адаптивность */
@media (max-width: 768px) {
  .announcement-card {
    padding: var(--spacing-md);
  }

  .announcement-card__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .announcement-card__meta {
    align-items: flex-start;
  }

  .announcement-card__images-grid {
    grid-template-columns: 1fr;
  }

  .announcement-card__footer {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: flex-start;
  }
}
</style> 