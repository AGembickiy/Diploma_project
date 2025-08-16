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
          sort-field="created_at"
          empty-icon="📋"
          empty-title="Нет объявлений"
          empty-description="У вас пока нет объявлений. Создайте первое объявление!"
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
import { ref, onMounted } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import AdvertisementCard from '@/components/advertisement/AdvertisementCard.vue'
import CreateAdvertisementDialog from '@/components/advertisement/CreateAdvertisementDialog.vue'
import EditAdvertisementDialog from '@/components/advertisement/EditAdvertisementDialog.vue'
import CardList from '@/components/ui/CardList.vue'
import { useUserStore } from '@/stores/user'
import type { Advertisement, AdvertisementCreate } from '@/types/advertisement'
import axios from 'axios'

const user = useUserStore()
const isDialogVisible = ref(false)
const isEditDialogVisible = ref(false)
const editingAdvertisement = ref<Advertisement | null>(null)
const userAdvertisements = ref<Advertisement[]>([])
const isLoading = ref(false)

// Загрузка объявлений пользователя
const loadUserAdvertisements = async () => {
  if (!user.isAuthenticated) return
  
  try {
    isLoading.value = true
    const response = await axios.get('http://localhost:8000/api/advertisements/', {
      headers: {
        'Authorization': `Token ${user.token}`
      }
    })
    // API возвращает объект с полем results для пагинации
    userAdvertisements.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки объявлений:', error)
    userAdvertisements.value = []
  } finally {
    isLoading.value = false
  }
}

// Загрузка при монтировании компонента
onMounted(() => {
  if (user.isAuthenticated) {
    loadUserAdvertisements()
  }
})

const openDialog = () => {
  isDialogVisible.value = true
}

const closeDialog = () => {
  isDialogVisible.value = false
}

const handleCreateAdvertisement = async (advertisement: AdvertisementCreate) => {
  try {
    const formData = new FormData()
    formData.append('title', advertisement.title)
    formData.append('description', advertisement.description)
    formData.append('category', advertisement.category)
    if (advertisement.image) {
      formData.append('image', advertisement.image)
    }
    if (advertisement.videoFile) {
      formData.append('video', advertisement.videoFile)
    }
    if (advertisement.audioFile) {
      formData.append('audio', advertisement.audioFile)
    }
    
    const response = await axios.post('http://localhost:8000/api/advertisements/', formData, {
      headers: {
        'Authorization': `Token ${user.token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Добавляем новое объявление в начало списка
    userAdvertisements.value.unshift(response.data)
    closeDialog()
  } catch (error) {
    console.error('Ошибка создания объявления:', error)
    alert('Ошибка создания объявления')
  }
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