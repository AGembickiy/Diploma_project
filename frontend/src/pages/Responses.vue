<template>
  <MainLayout>
    <div class="responses-content">
      <h1>Отклики</h1>
      <p>Здесь будут отображаться отклики пользователей.</p>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/components/Layout/MainLayout.vue'
</script>

<style scoped>
.responses-content {
  padding: 2rem;
  font-family: var(--font-family-body);
}
</style> 