<template>
  <MainLayout>
    <div class="w-full max-w-3xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-4">Отклики</h1>
      <p class="text-base text-muted">Здесь будут отображаться отклики пользователей.</p>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/components/layout/MainLayout.vue'
</script>

<style scoped>
.responses-content {
  padding: 2rem;
  font-family: var(--font-family-body);
}
</style> 