<template>
  <footer class="footer">
    <div class="footer-container">
      <span class="footer-author">Автор проекта: Александр Гембицкий</span>
      <a class="footer-github" href="https://github.com/agembickiy/Diploma_project" target="_blank" rel="noopener">
        <svg class="github-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true" style="vertical-align: middle; margin-right: 6px;"><path d="M12 0.297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.387 0.6 0.113 0.82-0.258 0.82-0.577 0-0.285-0.011-1.04-0.017-2.04-3.338 0.726-4.042-1.61-4.042-1.61-0.546-1.387-1.333-1.756-1.333-1.756-1.089-0.745 0.084-0.729 0.084-0.729 1.205 0.084 1.84 1.236 1.84 1.236 1.07 1.834 2.809 1.304 3.495 0.997 0.108-0.775 0.418-1.305 0.762-1.605-2.665-0.305-5.466-1.334-5.466-5.931 0-1.31 0.469-2.381 1.236-3.221-0.124-0.303-0.535-1.523 0.117-3.176 0 0 1.008-0.322 3.301 1.23 0.957-0.266 1.983-0.399 3.003-0.404 1.02 0.005 2.047 0.138 3.006 0.404 2.291-1.553 3.297-1.23 3.297-1.23 0.653 1.653 0.242 2.873 0.119 3.176 0.77 0.84 1.235 1.911 1.235 3.221 0 4.609-2.803 5.624-5.475 5.921 0.43 0.371 0.823 1.102 0.823 2.222 0 1.606-0.015 2.898-0.015 3.293 0 0.322 0.216 0.694 0.825 0.576C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
        <span>GitHub</span>
      </a>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component logic
</script>

<style scoped>
@import '@/assets/styles/base.css';
.footer {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  color: var(--text-secondary);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
}
.footer-container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 70px;
}
.footer-author {
  font-family: var(--font-family-body);
  font-size: var(--font-size-lg);
  color: var(--primary-color);
  margin-right: 16px;
}
.footer-text {
  font-family: var(--font-family-body);
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
}
.footer-github {
  display: flex;
  align-items: center;
  color: var(--primary-color);
  text-decoration: none;
  font-size: var(--font-size-lg);
  font-family: var(--font-family-body);
  transition: color var(--duration-fast) var(--ease-in-out);
}
.footer-github:hover {
  color: var(--primary-dark);
}
.github-icon {
  margin-right: 4px;
}
</style> 