<template>
  <footer class="footer">
    <div class="footer-container">
      <span class="footer-text">подвал</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component logic
</script>

<style scoped>
.footer {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  color: var(--text-secondary);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
}

.footer-container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: var(--spacing-xl) var(--container-padding);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60px;
}

.footer-text {
  font-family: var(--font-family-body);
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
}
</style> 