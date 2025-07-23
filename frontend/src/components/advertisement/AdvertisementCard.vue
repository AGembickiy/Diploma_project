<template>
  <div class="bg-secondary rounded-lg shadow-md overflow-hidden card-border">
    <div class="p-0 custom-padding relative">
      <div class="flex items-center gap-2 mb-4">
        <span class="px-2 py-1 text-xs rounded bg-primary text-white flex items-center gap-1">
          <img :src="getCategoryIcon(advertisement.category)" alt="" class="category-icon">
          {{ advertisement.category }}
        </span>
      </div>
      <h3 class="text-xl text-primary font-heading mb-4">{{ advertisement.title }}</h3>
      <p class="text-sm text-muted mb-4">{{ advertisement.description }}</p>
      
      <div v-if="advertisement.media" class="flex gap-2 mb-4">
        <span v-if="advertisement.media.images" class="text-xs text-muted flex items-center gap-1">
          <img src="@/assets/images/icons/board_icon.png" alt="" class="media-icon">
          {{ advertisement.media.images.length }}
        </span>
        <span v-if="advertisement.media.video" class="text-xs text-muted flex items-center gap-1">
          <img src="@/assets/images/icons/feedback_icon.png" alt="" class="media-icon">
          Видео
        </span>
        <span v-if="advertisement.media.audio" class="text-xs text-muted flex items-center gap-1">
          <img src="@/assets/images/icons/user_icon.png" alt="" class="media-icon">
          Аудио
        </span>
      </div>

      <div class="flex justify-between items-center mb-2">
        <span class="text-xs text-muted">{{ formatDate(advertisement.createdAt) }}</span>
      </div>
      <div class="ad-btns-block">
        <button class="ad-btn" title="Создать объявление">Создать</button>
        <button class="ad-btn" title="Редактировать объявление">Редактировать</button>
        <button class="ad-btn ad-btn-danger" title="Удалить объявление">Удалить</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Media {
  images?: string[]
  video?: string
  audio?: string
}

interface Advertisement {
  id: number
  title: string
  description: string
  category: 'Танки' | 'Хилы' | 'ДД' | 'Торговцы' | 'Гилдмастеры' | 'Квестгиверы' | 
             'Кузнецы' | 'Кожевники' | 'Зельевары' | 'Мастера заклинаний'
  image: string
  createdAt: string
  media?: Media
}

defineProps<{
  advertisement: Advertisement
}>()

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

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}
</script>

<style scoped>
.card-border {
  border: 2px solid rgb(162, 155, 254);
  position: relative;
  transition: all 0.3s ease;
  background-color: #2c2c44;
}

.card-border:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(162, 155, 254, 0.2);
}

.card-border::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 1px solid rgba(162, 155, 254, 0.3);
  border-radius: 8px;
  pointer-events: none;
}

.category-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.media-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.custom-padding {
  padding: 15px;
  position: relative;
}

.ad-btns-block {
  display: flex;
  gap: 12px;
  position: absolute;
  right: 15px;
  bottom: 15px;
}

.ad-btn {
  background: var(--primary-color, #a29bfe);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}
.ad-btn:hover {
  background: #6c63b5;
}
.ad-btn-danger {
  background: #ff7675;
}
.ad-btn-danger:hover {
  background: #d63031;
}
</style> 