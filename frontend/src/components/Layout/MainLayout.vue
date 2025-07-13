<template>
  <div class="main-layout">
    <Header />
    <div class="main-body">
      <ContentArea>
        <slot />
      </ContentArea>
      <Sidebar />
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/Layout/Header.vue'
import Sidebar from '@/components/Layout/Sidebar.vue'
import Footer from '@/components/Layout/Footer.vue'
import ContentArea from '@/components/Layout/ContentArea.vue'
</script>

<style src="@/assets/styles/layout.css" scoped /> 