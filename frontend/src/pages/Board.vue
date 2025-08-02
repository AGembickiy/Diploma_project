<template>
  <MainLayout>
    <div class="board-container">
      <div v-if="!user.isGuest" class="create-btn-container">
        <button class="create-btn" @click="openDialog" title="Создать объявление">Создать</button>
      </div>
      <div class="ad-list-wrapper">
        <CardList 
          :items="userAdvertisements"
          sort-by="date-desc"
          sort-field="createdAt"
          empty-icon="📋"
          empty-title="Нет объявлений"
          empty-description="У вас пока нет объявлений. Создайте первое объявление!"
          empty-action-link="#"
          empty-action-text="Создать объявление"
        >
          <template #default="{ item }">
            <AdvertisementCard
              :advertisement="item"
              @edit="handleEdit"
              @delete="handleDelete"
            />
          </template>
        </CardList>
      </div>
    </div>
    
    <CreateAdvertisementDialog 
      :is-visible="isDialogVisible"
      @close="closeDialog"
      @submit="handleCreateAdvertisement"
    />
    
    <EditAdvertisementDialog 
      :is-visible="isEditDialogVisible"
      :advertisement="editingAdvertisement"
      @close="closeEditDialog"
      @submit="handleEditSubmit"
    />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import AdvertisementCard from '@/components/advertisement/AdvertisementCard.vue'
import CreateAdvertisementDialog from '@/components/advertisement/CreateAdvertisementDialog.vue'
import EditAdvertisementDialog from '@/components/advertisement/EditAdvertisementDialog.vue'
import CardList from '@/components/ui/CardList.vue'
import { useUserStore } from '@/stores/user'
import type { Advertisement } from '@/types/advertisement'

const user = useUserStore()
const isDialogVisible = ref(false)
const isEditDialogVisible = ref(false)
const editingAdvertisement = ref<Advertisement | null>(null)

// Объявления пользователя (моковые данные)
const userAdvertisements = ref<Advertisement[]>([
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

const openDialog = () => {
  isDialogVisible.value = true
}

const closeDialog = () => {
  isDialogVisible.value = false
}

const handleCreateAdvertisement = (advertisement: Advertisement) => {
  // Добавляем новое объявление в начало списка
  userAdvertisements.value.unshift(advertisement)
  closeDialog()
}

const handleEdit = (advertisement: Advertisement) => {
  editingAdvertisement.value = advertisement
  isEditDialogVisible.value = true
}

const handleDelete = (advertisement: Advertisement) => {
  if (confirm('Вы уверены, что хотите удалить это объявление?')) {
    const index = userAdvertisements.value.findIndex(ad => ad.id === advertisement.id)
    if (index !== -1) {
      userAdvertisements.value.splice(index, 1)
    }
  }
}

const closeEditDialog = () => {
  isEditDialogVisible.value = false
  editingAdvertisement.value = null
}

const handleEditSubmit = (updatedAdvertisement: Advertisement) => {
  const index = userAdvertisements.value.findIndex(ad => ad.id === updatedAdvertisement.id)
  if (index !== -1) {
    userAdvertisements.value[index] = updatedAdvertisement
  }
  closeEditDialog()
}
</script>

<style scoped>
.create-btn-container {
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
  padding-bottom: 16px;
}

.create-btn {
  background: var(--primary-color, #a29bfe);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
  font-family: 'MedievalSharp', cursive;
}

.create-btn:hover {
  background: #6c63b5;
}

.board-container {
  width: 100%;
  max-width: 6xl;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.ad-list-wrapper {
  flex: 1;
  overflow: hidden;
}
</style> 