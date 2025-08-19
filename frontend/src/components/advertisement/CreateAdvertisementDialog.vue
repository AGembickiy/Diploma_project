<template>
  <div v-if="isVisible" class="dialog-overlay" @click="closeDialog">
    <div class="dialog-content" @click.stop>
      <div class="dialog-header">
        <h2 class="dialog-title">Создать объявление</h2>
        <button class="close-btn" @click="closeDialog" title="Закрыть">×</button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="dialog-form">
        <div class="form-group">
          <label for="title" class="form-label">Заголовок</label>
          <input 
            id="title"
            v-model="form.title"
            type="text" 
            class="form-input"
            placeholder="Введите заголовок объявления"
            required
          >
        </div>

        <div class="form-group">
          <label for="category" class="form-label">Категория</label>
          <select 
            id="category"
            v-model="form.category"
            class="form-select"
            required
          >
            <option value="">Выберите категорию</option>
            <option value="Танки">Танки</option>
            <option value="Хилы">Хилы</option>
            <option value="ДД">ДД</option>
            <option value="Торговцы">Торговцы</option>
            <option value="Гилдмастеры">Гилдмастеры</option>
            <option value="Квестгиверы">Квестгиверы</option>
            <option value="Кузнецы">Кузнецы</option>
            <option value="Кожевники">Кожевники</option>
            <option value="Зельевары">Зельевары</option>
            <option value="Мастера заклинаний">Мастера заклинаний</option>
          </select>
        </div>

        <div class="form-group">
          <label for="description" class="form-label">Описание</label>
          <textarea 
            id="description"
            v-model="form.description"
            class="form-textarea"
            placeholder="Введите описание объявления"
            rows="4"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">Медиа</label>
          <div class="media-options">
            <div class="media-section">
              <label class="media-label">Изображение</label>
              <input 
                id="image"
                type="file" 
                accept="image/*"
                @change="handleImageUpload"
                class="file-input"
              >
              <div v-if="form.image" class="file-item">
                <span>{{ form.image.name }}</span>
                <button type="button" @click="removeImage" class="remove-btn">×</button>
              </div>
            </div>

            <div class="media-section">
              <label class="media-label">Видео</label>
              <input 
                type="file" 
                accept="video/*"
                @change="handleVideoUpload"
                class="file-input"
              >
              <div v-if="form.videoFile" class="file-item">
                <span>{{ form.videoFile.name }}</span>
                <button type="button" @click="removeVideo" class="remove-btn">×</button>
              </div>
            </div>

            <div class="media-section">
              <label class="media-label">Аудио</label>
              <input 
                type="file" 
                accept="audio/*"
                @change="handleAudioUpload"
                class="file-input"
              >
              <div v-if="form.audioFile" class="file-item">
                <span>{{ form.audioFile.name }}</span>
                <button type="button" @click="removeAudio" class="remove-btn">×</button>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="closeDialog">
            Отмена
          </button>
          <button type="submit" class="btn btn-primary">
            Создать
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { AdvertisementCreate, AdvertisementCategory } from '@/types/advertisement'

interface Props {
  isVisible: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'submit', advertisement: AdvertisementCreate): void
}

const _props = defineProps<Props>()
const emit = defineEmits<Emits>()

const form = reactive({
  title: '',
  description: '',
  category: '' as AdvertisementCategory | '',
  image: undefined as File | undefined,
  videoFile: undefined as File | undefined,
  audioFile: undefined as File | undefined
})

const closeDialog = () => {
  // Сброс формы при закрытии
  form.title = ''
  form.description = ''
  form.category = ''
  form.image = undefined
  form.videoFile = undefined
  form.audioFile = undefined
  
  emit('close')
}

const handleSubmit = () => {
  if (!form.title || !form.description || !form.category) {
    return
  }

  const newAdvertisement: AdvertisementCreate = {
    title: form.title,
    description: form.description,
    category: form.category as AdvertisementCategory,
    image: form.image
  }

  emit('submit', newAdvertisement)
  closeDialog() // Используем closeDialog для сброса формы и закрытия
}

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    form.image = target.files[0];
  }
};

const removeImage = () => {
  form.image = undefined;
};

const handleVideoUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    form.videoFile = target.files[0];
  }
};

const removeVideo = () => {
  form.videoFile = undefined;
};

const handleAudioUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    form.audioFile = target.files[0];
  }
};

const removeAudio = () => {
  form.audioFile = undefined;
};
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

.form-input,
.form-textarea,
.form-select {
  background: var(--bg-primary, #1a1a2e);
  border: 1px solid var(--primary-color, #a29bfe);
  border-radius: 4px;
  padding: 8px 12px;
  color: var(--text-primary, #fff);
  font-size: 14px;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #6c63b5;
  box-shadow: 0 0 0 2px rgba(162, 155, 254, 0.2);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.media-options {
  display: flex;
  flex-direction: column; /* Changed to column to stack sections */
  gap: 16px;
}

.media-section {
  border: 1px solid var(--primary-color, #a29bfe);
  border-radius: 4px;
  padding: 12px;
  background: var(--bg-primary, #1a1a2e);
  width: 100%;
  box-sizing: border-box;
}

.media-label {
  color: var(--text-primary, #fff);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  display: block;
}

.file-input {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding: 8px 12px;
  background: var(--bg-secondary, #2c2c44);
  border: 1px solid var(--primary-color, #a29bfe);
  border-radius: 6px;
  color: var(--text-primary, #fff);
  font-size: 14px;
  font-family: 'MedievalSharp', cursive;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-input:hover {
  background: var(--bg-primary, #1a1a2e);
  border-color: #6c63b5;
}

.file-input:focus {
  outline: none;
  border-color: #6c63b5;
  box-shadow: 0 0 0 2px rgba(162, 155, 254, 0.2);
}

.file-input::file-selector-button {
  background: var(--primary-color, #a29bfe);
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  font-family: 'MedievalSharp', cursive;
  cursor: pointer;
  transition: background 0.2s;
  margin-right: 8px;
}

.file-input::file-selector-button:hover {
  background: #6c63b5;
}

.file-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-secondary, #2c2c44);
  border: 1px solid var(--primary-color, #a29bfe);
  border-radius: 4px;
  padding: 6px 8px;
  color: var(--text-primary, #fff);
  font-size: 12px;
}

.remove-btn {
  background: none;
  border: none;
  color: var(--text-muted, #888);
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.remove-btn:hover {
  background: rgba(162, 155, 254, 0.1);
  color: var(--text-primary, #fff);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary, #fff);
  font-size: 14px;
  cursor: pointer;
}

.form-checkbox {
  width: 16px;
  height: 16px;
  accent-color: var(--primary-color, #a29bfe);
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

.btn-primary {
  background: var(--primary-color, #a29bfe);
  color: #fff;
}

.btn-primary:hover {
  background: #6c63b5;
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