<template>
  <div class="home">
    <h1>Добро пожаловать в дипломный проект!</h1>
    
    <div class="features">
      <div class="feature-card">
        <h3>Vue 3</h3>
        <p>Современный фреймворк с Composition API</p>
      </div>
      
      <div class="feature-card">
        <h3>TypeScript</h3>
        <p>Строгая типизация для надежного кода</p>
      </div>
      
      <div class="feature-card">
        <h3>Pinia</h3>
        <p>Управление состоянием приложения</p>
      </div>
      
      <div class="feature-card">
        <h3>Vite</h3>
        <p>Быстрый инструмент сборки</p>
      </div>
    </div>
    
    <div class="tech-stack">
      <h2>Технологический стек:</h2>
      <ul>
        <li>Vue 3.3.4</li>
        <li>Vue Router 4.2.4</li>
        <li>Pinia 2.1.6</li>
        <li>TypeScript 5.1.6</li>
        <li>Vite 4.4.5</li>
        <li>Axios 1.5.0</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
// Composition API setup
</script>

<style scoped>
.home {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.home h1 {
  text-align: center;
  margin-bottom: var(--spacing-3xl);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: var(--font-family-heading);
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  letter-spacing: 0.05em;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-xl);
  margin: var(--spacing-3xl) 0;
}

.feature-card {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  text-align: center;
  transition: all var(--duration-normal) var(--ease-in-out);
  border: 1px solid var(--border-color);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  border-color: var(--primary-color);
}

.feature-card h3 {
  color: var(--primary-color);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family-heading);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.feature-card p {
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  font-family: var(--font-family-body);
}

.tech-stack {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  margin-top: var(--spacing-3xl);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.tech-stack h2 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  text-align: center;
  font-family: var(--font-family-heading);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.tech-stack ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.tech-stack li {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: var(--white);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  text-align: center;
  font-weight: var(--font-weight-medium);
  box-shadow: var(--shadow-sm);
  transition: all var(--duration-fast) var(--ease-in-out);
  font-family: var(--font-family-body);
}

.tech-stack li:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

/* Адаптивность */
@media (max-width: 768px) {
  .home {
    padding: var(--spacing-lg);
  }
  
  .features {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
  
  .tech-stack ul {
    grid-template-columns: 1fr;
  }
}
</style> 