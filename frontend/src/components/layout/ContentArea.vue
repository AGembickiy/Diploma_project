<template>
  <section class="content-area">
    <slot />
  </section>
</template>

<script setup lang="ts">
// ContentArea logic (if needed)
</script>

<style scoped>
.content-area {
  flex: 1 1 auto;
  padding: var(--container-padding);
  background: var(--bg-primary);
  font-family: var(--font-family-body);
  color: var(--text-primary);
  min-height: 0;
  box-sizing: border-box;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style> 