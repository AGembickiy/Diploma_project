<template>
  <div class="ad-list-container">
    <div class="ad-list-grid">
      <AdvertisementCard
        v-for="ad in advertisements"
        :key="ad.id"
        :advertisement="ad"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>
    
    <EditAdvertisementDialog 
      :is-visible="isEditDialogVisible"
      :advertisement="editingAdvertisement"
      @close="closeEditDialog"
      @submit="handleEditSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdvertisementCard from './AdvertisementCard.vue'
import EditAdvertisementDialog from './EditAdvertisementDialog.vue'
import type { Advertisement } from '@/types/advertisement'

interface Props {
  newAdvertisement?: Advertisement
}

const props = defineProps<Props>()

const advertisements = ref<Advertisement[]>([
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
  }
])

const isEditDialogVisible = ref(false)
const editingAdvertisement = ref<Advertisement | null>(null)

// Добавляем новое объявление в начало списка
const addAdvertisement = (advertisement: Advertisement) => {
  advertisements.value.unshift(advertisement)
}

// Обработчик редактирования объявления
const handleEdit = (advertisement: Advertisement) => {
  editingAdvertisement.value = advertisement
  isEditDialogVisible.value = true
}

// Обработчик удаления объявления
const handleDelete = (advertisement: Advertisement) => {
  // Удаляем объявление из списка
  const index = advertisements.value.findIndex(ad => ad.id === advertisement.id)
  if (index !== -1) {
    advertisements.value.splice(index, 1)
  }
}

// Закрытие диалога редактирования
const closeEditDialog = () => {
  isEditDialogVisible.value = false
  editingAdvertisement.value = null
}

// Обработчик сохранения изменений
const handleEditSubmit = (updatedAdvertisement: Advertisement) => {
  const index = advertisements.value.findIndex(ad => ad.id === updatedAdvertisement.id)
  if (index !== -1) {
    advertisements.value[index] = updatedAdvertisement
  }
  closeEditDialog()
}

// Экспортируем функцию для использования в родительском компоненте
defineExpose({
  addAdvertisement
})
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