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

// emit response больше не нужен
const props = defineProps<Props>()
// emit больше не нужен
const user = useUserStore()

// Фильтруем объявления - исключаем объявления текущего пользователя
const publicAdvertisements = computed(() => {
  // Если пользователь гость, показываем все объявления
  if (user.isGuest) {
    return props.advertisements
  }
  
  // Для авторизованных пользователей исключаем их собственные объявления
  return props.advertisements.filter(ad => ad.author?.id !== user.user?.id)
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