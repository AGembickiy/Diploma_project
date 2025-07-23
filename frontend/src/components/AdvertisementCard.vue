<template>
  <div class="advertisement-card">
    <div class="advertisement-card__image">
      <img :src="advertisement.images[0]" :alt="advertisement.title">
    </div>
    <div class="advertisement-card__content">
      <h3 class="advertisement-card__title">{{ advertisement.title }}</h3>
      <p class="advertisement-card__price">{{ formatPrice(advertisement.price) }} ₽</p>
      <p class="advertisement-card__location">{{ advertisement.location }}</p>
      <p class="advertisement-card__date">{{ formatDate(advertisement.createdAt) }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Advertisement } from '@/types/advertisement'

defineProps<{
  advertisement: Advertisement
}>()

const formatPrice = (price: number): string => {
  return price.toLocaleString('ru-RU')
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
.advertisement-card {
  background-color: #2c2c44;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease;
}

.advertisement-card:hover {
  transform: translateY(-2px);
}

.advertisement-card__image {
  height: 200px;
  overflow: hidden;
}

.advertisement-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.advertisement-card__content {
  padding: 16px;
}

.advertisement-card__title {
  font-family: 'MedievalSharp', cursive;
  color: rgb(162, 155, 254);
  font-size: 18px;
  margin: 0 0 8px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.advertisement-card__price {
  color: #42b983;
  font-size: 20px;
  font-weight: bold;
  margin: 0 0 8px;
}

.advertisement-card__location {
  color: #8a8a8a;
  font-size: 14px;
  margin: 0 0 4px;
}

.advertisement-card__date {
  color: #666;
  font-size: 12px;
  margin: 0;
}
</style> 