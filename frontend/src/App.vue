<template>
  <div id="app">
    <Header />
    
    <div class="app-layout">
      <Sidebar />
      <main class="app-main">
        <router-view />
      </main>
    </div>
    
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/Layout/Header.vue'
import Footer from '@/components/Layout/Footer.vue'
import Sidebar from '@/components/Layout/Sidebar.vue'
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-primary);
}

.app-layout {
  display: flex;
  flex: 1;
  margin-top: 70px; /* Высота хедера */
}

.app-main {
  flex: 1;
  padding: var(--spacing-xl);
  margin-left: 280px; /* Ширина сайдбара */
  background-color: var(--bg-primary);
  min-height: calc(100vh - 70px); /* Высота минус хедер */
}

/* Адаптивность */
@media (max-width: 768px) {
  .app-layout {
    margin-top: 0;
  }
  
  .app-main {
    margin-left: 0;
    padding: var(--spacing-lg);
    min-height: calc(100vh - 70px);
  }
}
</style> 