<template>
  <div v-if="isVisible" class="dialog-overlay" @click="closeDialog">
    <div class="dialog-content" @click.stop>
      <div class="dialog-header">
        <h2 class="dialog-title">Отклик на объявление</h2>
        <button class="close-btn" @click="closeDialog" title="Закрыть">×</button>
      </div>
      
      <div class="advertisement-preview">
        <h3 class="ad-title">{{ advertisement?.title }}</h3>
        <p class="ad-category">{{ advertisement?.category }}</p>
        <p class="ad-description">{{ advertisement?.description }}</p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="dialog-form">
        <div class="form-group">
          <label for="response-text" class="form-label">Ваше сообщение</label>
          <textarea 
            id="response-text"
            v-model="responseText"
            class="form-textarea"
            placeholder="Напишите ваш отклик на объявление..."
            rows="6"
            required
            maxlength="1000"
          ></textarea>
          <div class="char-counter">
            {{ responseText.length }}/1000 символов
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="closeDialog">
            Отмена
          </button>
          <button type="submit" class="btn btn-primary" :disabled="!responseText.trim()">
            Отправить отклик
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Advertisement } from '@/types/advertisement'

interface Props {
  isVisible: boolean
  advertisement: Advertisement | null
}

interface Emits {
  (e: 'close'): void
  (e: 'submit', response: { advertisementId: number; text: string }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const responseText = ref('')

// Сброс формы при открытии диалога и закрытие при изменении isVisible на false
watch(() => props.isVisible, (isVisible) => {
  if (isVisible) {
    responseText.value = ''
  } else {
    // Если диалог скрывается, сбрасываем форму
    responseText.value = ''
  }
})

const closeDialog = () => {
  responseText.value = '' // Сбрасываем форму
  emit('close')
}

const handleSubmit = () => {
  if (!responseText.value.trim() || !props.advertisement) {
    return
  }

  const response = {
    advertisementId: props.advertisement.id,
    text: responseText.value.trim()
  }

  emit('submit', response)
  
  // Закрываем диалог после отправки отклика
  closeDialog()
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.dialog-content {
  background: var(--bg-secondary, #2c2c44);
  border: 2px solid var(--primary-color, #a29bfe);
  border-radius: 8px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dialog-title {
  color: var(--text-primary, #fff);
  font-family: 'MedievalSharp', cursive;
  font-size: 20px;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-muted, #888);
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(162, 155, 254, 0.1);
  color: var(--text-primary, #fff);
}

.advertisement-preview {
  background: var(--bg-primary, #1a1a2e);
  border: 1px solid var(--primary-color, #a29bfe);
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 20px;
}

.ad-title {
  color: var(--primary-color, #a29bfe);
  font-family: 'MedievalSharp', cursive;
  font-size: 18px;
  margin: 0 0 8px 0;
}

.ad-category {
  color: var(--text-secondary, #b8b8b8);
  font-size: 14px;
  margin: 0 0 8px 0;
  font-weight: 500;
}

.ad-description {
  color: var(--text-primary, #fff);
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: var(--text-primary, #fff);
  font-size: 14px;
  font-weight: 500;
}

.form-textarea {
  background: var(--bg-primary, #1a1a2e);
  border: 1px solid var(--primary-color, #a29bfe);
  border-radius: 4px;
  padding: 12px;
  color: var(--text-primary, #fff);
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
  transition: all 0.2s;
}

.form-textarea:focus {
  outline: none;
  border-color: #6c63b5;
  box-shadow: 0 0 0 2px rgba(162, 155, 254, 0.2);
}

.char-counter {
  text-align: right;
  font-size: 12px;
  color: var(--text-muted, #888);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
  font-family: 'MedievalSharp', cursive;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--success-color, #00b894);
  color: #fff;
}

.btn-primary:hover:not(:disabled) {
  background: #00a085;
}

.btn-secondary {
  background: transparent;
  color: var(--text-muted, #888);
  border: 1px solid var(--text-muted, #888);
}

.btn-secondary:hover {
  background: rgba(136, 136, 136, 0.1);
  color: var(--text-primary, #fff);
}
</style> 