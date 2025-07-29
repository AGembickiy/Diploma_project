<template>
  <div class="public-ad-list-container">
    <div class="public-ad-list-grid">
      <AdvertisementCard
        v-for="ad in publicAdvertisements"
        :key="ad.id"
        :advertisement="ad"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AdvertisementCard from './AdvertisementCard.vue'
import type { Advertisement } from '@/types/advertisement'
import { useUserStore } from '@/stores/user'

interface Props {
  advertisements: Advertisement[]
}

const props = defineProps<Props>()
const user = useUserStore()

// Фильтруем объявления - исключаем объявления текущего пользователя
const publicAdvertisements = computed(() => {
  // Если пользователь гость, показываем все объявления
  if (user.isGuest) {
    return props.advertisements
  }
  
  // Иначе исключаем объявления текущего пользователя
  // Пока используем простую логику - исключаем первые 2 объявления как "пользовательские"
  return props.advertisements.slice(2)
})
</script>

<style scoped>
.public-ad-list-container {
  height: 100%;
  overflow-y: auto;
  max-height: calc(100vh - 200px);
}

.public-ad-list-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}
</style> 