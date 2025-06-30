<template>
  <div class="about">
    <h1>О дипломном проекте</h1>
    
    <div class="project-info">
      <h2>Описание проекта</h2>
      <p>
        Данный проект представляет собой современное веб-приложение, 
        разработанное с использованием передовых технологий фронтенд-разработки.
      </p>
      
      <h2>Архитектура</h2>
      <p>
        Проект построен на основе модульной архитектуры с четким разделением 
        ответственности между компонентами и использованием современных паттернов разработки.
      </p>
      
      <h2>Основные принципы</h2>
      <ul>
        <li>TypeScript First - строгая типизация</li>
        <li>Composition API - современный подход Vue 3</li>
        <li>Модульность - четкое разделение кода</li>
        <li>Переиспользуемость - компонентный подход</li>
      </ul>
    </div>
    
    <div class="architecture-diagram">
      <h2>Структура проекта</h2>
      <pre><code>
src/
├── assets/          # Статические ресурсы
├── components/      # Vue компоненты
├── composables/     # Composition API hooks
├── pages/          # Страницы приложения
├── router/         # Конфигурация роутинга
├── services/       # API сервисы
├── stores/         # Pinia stores
├── types/          # TypeScript типы
└── utils/          # Утилиты
      </code></pre>
    </div>
  </div>
</template>

<script setup lang="ts">
// Composition API setup
</script>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.about h1 {
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

.project-info {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  margin: var(--spacing-xl) 0;
  border: 1px solid var(--border-color);
}

.project-info h2 {
  color: var(--primary-color);
  margin-top: var(--spacing-xl);
  margin-bottom: var(--spacing-md);
  font-family: var(--font-family-heading);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.project-info h2:first-child {
  margin-top: 0;
}

.project-info p {
  color: var(--text-secondary);
  font-family: var(--font-family-body);
  line-height: var(--line-height-relaxed);
}

.project-info ul {
  margin-left: var(--spacing-xl);
  color: var(--text-secondary);
  font-family: var(--font-family-body);
}

.project-info li {
  margin: var(--spacing-sm) 0;
  line-height: var(--line-height-relaxed);
}

.architecture-diagram {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  margin-top: var(--spacing-xl);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.architecture-diagram h2 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  font-family: var(--font-family-heading);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.architecture-diagram pre {
  background: #2d3748;
  color: #e2e8f0;
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-md);
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: var(--font-size-sm);
  line-height: 1.4;
  box-shadow: var(--shadow-sm);
}

/* Адаптивность */
@media (max-width: 768px) {
  .about {
    padding: var(--spacing-lg);
  }
  
  .project-info,
  .architecture-diagram {
    padding: var(--spacing-lg);
  }
}
</style> 