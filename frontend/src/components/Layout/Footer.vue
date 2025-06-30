<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">Дипломный проект</h3>
          <p class="footer-description">
            Современное веб-приложение, разработанное с использованием 
            передовых технологий фронтенд-разработки.
          </p>
          <div class="social-links">
            <a href="#" class="social-link" title="GitHub">
              <span class="social-icon">📚</span>
            </a>
            <a href="#" class="social-link" title="LinkedIn">
              <span class="social-icon">💼</span>
            </a>
            <a href="#" class="social-link" title="Email">
              <span class="social-icon">✉️</span>
            </a>
          </div>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-subtitle">Навигация</h4>
          <ul class="footer-links">
            <li><router-link to="/" class="footer-link">Главная</router-link></li>
            <li><router-link to="/about" class="footer-link">О проекте</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-subtitle">Технологии</h4>
          <ul class="footer-links">
            <li><span class="footer-link">Vue 3</span></li>
            <li><span class="footer-link">TypeScript</span></li>
            <li><span class="footer-link">Pinia</span></li>
            <li><span class="footer-link">Vite</span></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-subtitle">Контакты</h4>
          <ul class="footer-links">
            <li><span class="footer-link">📧 info@diploma.com</span></li>
            <li><span class="footer-link">📱 +7 (999) 123-45-67</span></li>
            <li><span class="footer-link">📍 Москва, Россия</span></li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <div class="footer-bottom-content">
          <p class="copyright">
            &copy; 2024 Дипломный проект. Все права защищены.
          </p>
          <div class="footer-bottom-links">
            <a href="#" class="footer-bottom-link">Политика конфиденциальности</a>
            <a href="#" class="footer-bottom-link">Условия использования</a>
          </div>
        </div>
      </div>
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
  padding: 0 var(--container-padding);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  padding: var(--spacing-3xl) 0 var(--spacing-xl);
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.footer-title {
  color: var(--text-primary);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family-heading);
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.footer-subtitle {
  color: var(--primary-color);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family-heading);
  margin: 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.footer-description {
  color: var(--text-secondary);
  font-family: var(--font-family-body);
  line-height: var(--line-height-relaxed);
  margin: 0;
}

.social-links {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-in-out);
}

.social-link:hover {
  color: var(--primary-color);
  background: var(--bg-secondary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.social-icon {
  font-size: var(--font-size-lg);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.footer-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-family: var(--font-family-body);
  transition: color var(--duration-fast) var(--ease-in-out);
  display: inline-block;
}

.footer-link:hover {
  color: var(--primary-color);
}

.footer-bottom {
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-lg) 0;
}

.footer-bottom-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.copyright {
  color: var(--text-muted);
  font-family: var(--font-family-body);
  margin: 0;
  font-size: var(--font-size-sm);
}

.footer-bottom-links {
  display: flex;
  gap: var(--spacing-lg);
}

.footer-bottom-link {
  color: var(--text-muted);
  text-decoration: none;
  font-family: var(--font-family-body);
  font-size: var(--font-size-sm);
  transition: color var(--duration-fast) var(--ease-in-out);
}

.footer-bottom-link:hover {
  color: var(--primary-color);
}

/* Адаптивность */
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
    padding: var(--spacing-xl) 0 var(--spacing-lg);
  }
  
  .footer-bottom-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-bottom-links {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .footer-container {
    padding: 0 var(--spacing-md);
  }
  
  .footer-title {
    font-size: var(--font-size-lg);
  }
  
  .footer-subtitle {
    font-size: var(--font-size-base);
  }
}
</style> 