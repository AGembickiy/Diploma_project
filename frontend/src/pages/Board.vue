<template>
  <MainLayout>
    <div v-if="!user.isGuest" class="create-btn-container">
      <button class="create-btn" title="Создать объявление">Создать</button>
    </div>
    <div class="board-container">
      <div class="ad-list-wrapper">
        <AdvertisementList />
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/components/layout/MainLayout.vue'
import AdvertisementList from '@/components/advertisement/AdvertisementList.vue'
import { useUserStore } from '@/stores/user'

const user = useUserStore()
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