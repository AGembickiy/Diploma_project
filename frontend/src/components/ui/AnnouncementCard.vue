<template>
  <div :class="['rounded-lg shadow-md p-4 mb-4 bg-tertiary text-foreground transition', !announcement.isActive ? 'opacity-60 grayscale' : '']">
    <!-- Заголовок карточки -->
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center gap-2">
        <img :src="categoryInfo.icon" :alt="categoryInfo.label" class="w-8 h-8 object-contain" loading="lazy" />
        <span class="font-medium text-base">{{ categoryInfo.label }}</span>
      </div>
      <div class="flex flex-col items-end text-xs text-muted">
        <span>{{ announcement.author }}</span>
        <span>{{ formattedDate }}</span>
      </div>
    </div>
    <h3 class="text-xl font-bold mb-2">{{ announcement.title }}</h3>
    <div class="mb-2 whitespace-pre-line">{{ announcement.content }}</div>
    <div v-if="announcement.images && announcement.images.length" class="flex gap-2 flex-wrap mb-2">
      <img v-for="(img, idx) in announcement.images" :key="idx" :src="img" alt="Изображение объявления" class="w-32 h-24 object-cover rounded" loading="lazy" />
    </div>
    <div v-if="announcement.videos && announcement.videos.length" class="flex gap-2 flex-wrap mb-2">
      <video v-for="(vid, idx) in announcement.videos" :key="idx" :src="vid" controls class="w-40 h-28 rounded" preload="metadata" />
    </div>
    <div class="flex items-center justify-between mt-4">
      <span :class="['inline-block px-3 py-1 rounded text-xs font-semibold', announcement.isActive ? 'bg-success text-white' : 'bg-error text-white']">
        {{ announcement.isActive ? 'Активно' : 'Неактивно' }}
      </span>
      <button v-if="announcement.updatedAt" @click="showUpdateInfo" class="text-xs text-info underline hover:text-primary focus:outline-none focus:ring-2 focus:ring-info rounded" aria-label="Информация об обновлении" tabindex="0">
        Обновлено {{ formatUpdateDate }}
      </button>
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

function showUpdateInfo() {
  // Можно реализовать показ модального окна с историей изменений
  alert('Объявление обновлено: ' + formatUpdateDate.value)
}
</script> 