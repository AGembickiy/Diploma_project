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
    
    <ConfirmationDialog
      :is-visible="showDeleteConfirm"
      title="Удалить объявление"
      message="Вы уверены, что хотите удалить это объявление? Это действие необратимо."
      confirm-text="Удалить"
      cancel-text="Отмена"
      :show-cancel="true"
      @confirm="confirmDelete"
      @close="showDeleteConfirm = false"
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
import ConfirmationDialog from '@/components/advertisement/ConfirmationDialog.vue'
import { useUserStore } from '@/stores/user'
import type { Advertisement, AdvertisementCreate } from '@/types/advertisement'
import axios from 'axios'

const user = useUserStore()
const isDialogVisible = ref(false)
const isEditDialogVisible = ref(false)
const editingAdvertisement = ref<Advertisement | null>(null)
const userAdvertisements = ref<Advertisement[]>([])
const isLoading = ref(false)
const showDeleteConfirm = ref(false)
const deletingAdvertisement = ref<Advertisement | null>(null)

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
    const advertisements = response.data.results || response.data

    
    // Проверяем, что у каждого объявления есть информация об авторе
    advertisements.forEach((ad: any, index: number) => {
      // Логика проверки автора
    })
    
    userAdvertisements.value = advertisements
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
    
    // Добавляем новое объявление в начало списка с информацией об авторе
    const newAdvertisement = {
      ...response.data,
      author: {
        id: user.user?.id,
        username: user.user?.username || user.user?.email,
        email: user.user?.email
      }
    }

    userAdvertisements.value.unshift(newAdvertisement)
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

const handleDelete = async (advertisement: Advertisement) => {
  // Показываем диалог подтверждения
  showDeleteConfirm.value = true
  deletingAdvertisement.value = advertisement
}

const closeEditDialog = () => {
  isEditDialogVisible.value = false
  editingAdvertisement.value = null
}

const confirmDelete = async () => {
  if (!deletingAdvertisement.value) return
  
  try {
    await axios.delete(`http://localhost:8000/api/advertisements/${deletingAdvertisement.value.id}/`, {
      headers: {
        'Authorization': `Token ${user.token}`
      }
    })
    
    // Удаляем из локального списка только после успешного удаления на сервере
    const index = userAdvertisements.value.findIndex(ad => ad.id === deletingAdvertisement.value?.id)
    if (index !== -1) {
      userAdvertisements.value.splice(index, 1)
    }
    
    showDeleteConfirm.value = false
    deletingAdvertisement.value = null
  } catch (error) {
    console.error('Ошибка удаления объявления:', error)
    alert('Ошибка удаления объявления')
  }
}

const handleEditSubmit = async (updatedAdvertisement: Advertisement) => {
  try {
    const formData = new FormData()
    formData.append('title', updatedAdvertisement.title)
    formData.append('description', updatedAdvertisement.description)
    formData.append('category', updatedAdvertisement.category)
    
    // Безопасная проверка файлов
    const image = (updatedAdvertisement as any).image
    const videoFile = (updatedAdvertisement as any).videoFile
    const audioFile = (updatedAdvertisement as any).audioFile
    
    if (image && typeof image === 'object' && 'size' in image) {
      formData.append('image', image)
    }
    if (videoFile && typeof videoFile === 'object' && 'size' in videoFile) {
      formData.append('video', videoFile)
    }
    if (audioFile && typeof audioFile === 'object' && 'size' in audioFile) {
      formData.append('audio', audioFile)
    }
    
    const response = await axios.put(`http://localhost:8000/api/advertisements/${updatedAdvertisement.id}/`, formData, {
      headers: {
        'Authorization': `Token ${user.token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Обновляем локальный список только после успешного обновления на сервере
    const index = userAdvertisements.value.findIndex(ad => ad.id === updatedAdvertisement.id)
    if (index !== -1) {
      const updatedAd = {
        ...response.data,
        author: {
          id: user.user?.id,
          username: user.user?.username || user.user?.email,
          email: user.user?.email
        }
      }
  
      userAdvertisements.value[index] = updatedAd
    }
    
    closeEditDialog()
  } catch (error) {
    console.error('Ошибка обновления объявления:', error)
    alert('Ошибка обновления объявления')
  }
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