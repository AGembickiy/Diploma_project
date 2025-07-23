<template>
  <div class="advertisement-list">
    <h1 class="advertisement-list__title">Объявления</h1>
    
    <div class="advertisement-list__grid">
      <AdvertisementCard
        v-for="ad in advertisements"
        :key="ad.id"
        :advertisement="ad"
        class="advertisement-list__item"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Advertisement } from '@/types/advertisement'
import AdvertisementCard from '@/components/AdvertisementCard.vue'

// Временные данные для тестирования
const advertisements = ref<Advertisement[]>([
  {
    id: 1,
    title: 'iPhone 13 Pro Max',
    description: 'Отличное состояние, полный комплект',
    price: 75000,
    location: 'Москва',
    category: 'Электроника',
    images: ['https://picsum.photos/400/300'],
    createdAt: '2024-03-20T10:00:00',
    author: {
      id: 1,
      name: 'Александр',
      phone: '+7 (999) 123-45-67'
    }
  },
  {
    id: 2,
    title: 'Велосипед Giant',
    description: 'Горный велосипед, 21 скорость',
    price: 45000,
    location: 'Санкт-Петербург',
    category: 'Спорт и отдых',
    images: ['https://picsum.photos/400/300'],
    createdAt: '2024-03-19T15:30:00',
    author: {
      id: 2,
      name: 'Мария',
      phone: '+7 (999) 765-43-21'
    }
  }
])
</script>

<style scoped lang="scss">
@import "@/assets/styles/variables.scss";

.advertisement-list {
  padding: $spacing-lg;

  &__title {
    font-size: $font-size-2xl;
    font-weight: 700;
    margin-bottom: $spacing-lg;
    color: $color-text-primary;
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: $spacing-lg;
  }

  &__item {
    width: 100%;
  }
}
</style> 