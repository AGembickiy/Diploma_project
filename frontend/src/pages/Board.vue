<template>
  <MainLayout>
    <div class="board-container">
      <div v-if="!user.isGuest" class="create-btn-container">
        <button class="create-btn" @click="openDialog" title="Создать объявление">Создать</button>
      </div>
      <div class="ad-list-wrapper">
        <AdvertisementList ref="advertisementListRef" />
      </div>
    </div>
    
    <CreateAdvertisementDialog 
      :is-visible="isDialogVisible"
      @close="closeDialog"
      @submit="handleCreateAdvertisement"
    />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import AdvertisementList from '@/components/advertisement/AdvertisementList.vue'
import CreateAdvertisementDialog from '@/components/advertisement/CreateAdvertisementDialog.vue'
import { useUserStore } from '@/stores/user'
import type { Advertisement } from '@/types/advertisement'

const user = useUserStore()
const isDialogVisible = ref(false)
const advertisementListRef = ref()

const openDialog = () => {
  isDialogVisible.value = true
}

const closeDialog = () => {
  isDialogVisible.value = false
}

const handleCreateAdvertisement = (advertisement: Advertisement) => {
  // Добавляем новое объявление в список
  if (advertisementListRef.value) {
    advertisementListRef.value.addAdvertisement(advertisement)
  }
  
  // Закрываем диалог
  closeDialog()
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