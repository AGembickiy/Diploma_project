<template>
  <div class="ad-list-container">
    <div class="ad-list-grid">
      <AdvertisementCard
        v-for="ad in advertisements"
        :key="ad.id"
        :advertisement="ad"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import AdvertisementCard from './AdvertisementCard.vue'
import type { Advertisement } from '@/types/advertisement'

const advertisements: Advertisement[] = [
  {
    id: 1,
    title: 'Опытный танк ищет гильдию',
    description: 'Танк 80 уровня с полным комплектом эпического снаряжения. Есть опыт всех рейдов. Готов к долгосрочному сотрудничеству.',
    category: 'Танки',
    image: '/images/tank.jpg',
    createdAt: new Date('2024-03-20'),
    media: {
      images: ['/images/tank1.jpg', '/images/tank2.jpg'],
      video: true
    }
  },
  {
    id: 2,
    title: 'Гильдмастер набирает команду',
    description: 'Собираю команду для новой гильдии. Нужны активные игроки всех классов. Есть свой Discord сервер.',
    category: 'Гилдмастеры',
    image: '/images/guild.jpg',
    createdAt: new Date('2024-03-19'),
    media: {
      images: ['/images/guild1.jpg'],
      video: true,
      audio: true
    }
  },
  {
    id: 3,
    title: 'Зельевар ищет заказы',
    description: 'Варю все виды зелий. Большой опыт, лучшие ингредиенты. Оптовые заказы приветствуются.',
    category: 'Зельевары',
    image: '/images/potion.jpg',
    createdAt: new Date('2024-03-18'),
    media: {
      images: ['/images/potion1.jpg', '/images/potion2.jpg', '/images/potion3.jpg']
    }
  }
]
</script>

<style scoped>
.ad-list-container {
  height: 100%;
  overflow-y: auto;
  max-height: calc(100vh - 200px);
}

.ad-list-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}
</style> 