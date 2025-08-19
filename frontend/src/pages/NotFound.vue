<template>
  <div class="flex items-center justify-center min-h-[60vh] text-center">
    <div class="flex flex-col items-center gap-4">
      <h1 class="text-6xl text-primary font-bold font-heading drop-shadow m-0">404</h1>
      <h2 class="text-2xl text-foreground font-heading drop-shadow m-0">Страница не найдена</h2>
      <p class="text-lg text-muted font-serif mb-6 leading-relaxed">К сожалению, запрашиваемая страница не существует.</p>
      <div class="flex gap-4 flex-wrap justify-center">
        <router-link to="/" class="px-6 py-3 rounded bg-primary text-white font-medium transition hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary" aria-label="Вернуться на главную" tabindex="0">Вернуться на главную</router-link>
        <button @click="goBack" class="px-6 py-3 rounded bg-secondary text-foreground font-medium transition hover:bg-tertiary focus:outline-none focus:ring-2 focus:ring-secondary" aria-label="Назад" tabindex="0">Назад</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.not-found {
  padding: 40px;
  text-align: center;
}

h1 {
  font-size: 48px;
  color: #2c3e50;
  margin-bottom: 16px;
}

p {
  color: #666;
  margin-bottom: 24px;
}

.back-link {
  color: #42b983;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}
</style> 