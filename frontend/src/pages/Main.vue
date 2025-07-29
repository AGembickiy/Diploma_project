<template>
  <MainLayout>
    <div class="main-container">
      <div class="ad-list-wrapper">
        <PublicAdvertisementList :advertisements="allAdvertisements" />
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import PublicAdvertisementList from '@/components/advertisement/PublicAdvertisementList.vue'
import type { Advertisement } from '@/types/advertisement'

// Все объявления (включая пользовательские)
const allAdvertisements = ref<Advertisement[]>([
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
  },
  {
    id: 4,
    title: 'Хил ищет статик',
    description: 'Опытный хил 85 уровня. Ищу статик для рейдов. Есть опыт всех контентов.',
    category: 'Хилы',
    image: '/images/healer.jpg',
    createdAt: new Date('2024-03-17'),
    media: {
      images: ['/images/healer1.jpg'],
      video: true
    }
  },
  {
    id: 5,
    title: 'ДД на заказы',
    description: 'ДД 90 уровня. Готов на любые заказы. Быстро и качественно.',
    category: 'ДД',
    image: '/images/dd.jpg',
    createdAt: new Date('2024-03-16'),
    media: {
      images: ['/images/dd1.jpg', '/images/dd2.jpg']
    }
  }
])
</script>

<style scoped>
.main-container {
  width: 100%;
  max-width: 6xl;
  margin: 0 auto;
  padding: 2rem 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.ad-list-wrapper {
  flex: 1;
  overflow: hidden;
}

@media (max-width: 900px) {
  .main-body {
    flex-direction: column;
  }
  :deep(.sidebar) {
    width: 100% !important;
    height: auto !important;
    position: relative !important;
  }
}
</style> 