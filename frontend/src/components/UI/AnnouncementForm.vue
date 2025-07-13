<template>
  <div class="announcement-form">
    <h2 class="announcement-form__title">
      {{ isEditing ? 'Редактировать объявление' : 'Создать объявление' }}
    </h2>

    <form @submit.prevent="handleSubmit" class="announcement-form__form">
      <!-- Выбор категории -->
      <div class="announcement-form__field">
        <label class="announcement-form__label">Категория *</label>
        <div class="announcement-form__category-grid">
          <div
            v-for="category in ANNOUNCEMENT_CATEGORIES"
            :key="category.value"
            class="announcement-form__category-option"
            :class="{ 'announcement-form__category-option--selected': form.category === category.value }"
            @click="selectCategory(category.value)"
          >
            <img 
              :src="category.icon" 
              :alt="category.label"
              class="announcement-form__category-icon"
            />
            <span class="announcement-form__category-label">{{ category.label }}</span>
          </div>
        </div>
        <span v-if="errors.category" class="announcement-form__error">{{ errors.category }}</span>
      </div>

      <!-- Заголовок -->
      <div class="announcement-form__field">
        <label for="title" class="announcement-form__label">Заголовок *</label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          class="announcement-form__input"
          :class="{ 'announcement-form__input--error': errors.title }"
          placeholder="Введите заголовок объявления"
          maxlength="100"
        />
        <span v-if="errors.title" class="announcement-form__error">{{ errors.title }}</span>
        <span class="announcement-form__counter">{{ form.title.length }}/100</span>
      </div>

      <!-- Контент -->
      <div class="announcement-form__field">
        <label for="content" class="announcement-form__label">Содержание *</label>
        <textarea
          id="content"
          v-model="form.content"
          class="announcement-form__textarea"
          :class="{ 'announcement-form__textarea--error': errors.content }"
          placeholder="Опишите ваше объявление. Поддерживается разметка: **жирный**, *курсив*"
          rows="8"
          maxlength="2000"
        ></textarea>
        <span v-if="errors.content" class="announcement-form__error">{{ errors.content }}</span>
        <span class="announcement-form__counter">{{ form.content.length }}/2000</span>
      </div>

      <!-- Загрузка изображений -->
      <div class="announcement-form__field">
        <label class="announcement-form__label">Изображения</label>
        <div class="announcement-form__file-upload">
          <input
            ref="imageInput"
            type="file"
            accept="image/*"
            multiple
            @change="handleImageUpload"
            class="announcement-form__file-input"
          />
          <div class="announcement-form__file-dropzone" @click="$refs.imageInput.click()">
            <div class="announcement-form__file-icon">📷</div>
            <p class="announcement-form__file-text">Нажмите для выбора изображений или перетащите файлы</p>
          </div>
        </div>
        
        <!-- Предварительный просмотр изображений -->
        <div v-if="form.images.length > 0" class="announcement-form__images-preview">
          <div 
            v-for="(image, index) in form.images" 
            :key="index"
            class="announcement-form__image-preview"
          >
            <img :src="image" :alt="`Изображение ${index + 1}`" />
            <button 
              type="button"
              class="announcement-form__image-remove"
              @click="removeImage(index)"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <!-- Загрузка видео -->
      <div class="announcement-form__field">
        <label class="announcement-form__label">Видео</label>
        <div class="announcement-form__file-upload">
          <input
            ref="videoInput"
            type="file"
            accept="video/*"
            multiple
            @change="handleVideoUpload"
            class="announcement-form__file-input"
          />
          <div class="announcement-form__file-dropzone" @click="$refs.videoInput.click()">
            <div class="announcement-form__file-icon">🎥</div>
            <p class="announcement-form__file-text">Нажмите для выбора видео или перетащите файлы</p>
          </div>
        </div>
        
        <!-- Список видео -->
        <div v-if="form.videos.length > 0" class="announcement-form__videos-list">
          <div 
            v-for="(video, index) in form.videos" 
            :key="index"
            class="announcement-form__video-item"
          >
            <span class="announcement-form__video-name">{{ getFileName(video) }}</span>
            <button 
              type="button"
              class="announcement-form__video-remove"
              @click="removeVideo(index)"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <!-- Кнопки действий -->
      <div class="announcement-form__actions">
        <button 
          type="button" 
          class="announcement-form__btn announcement-form__btn--secondary"
          @click="$emit('cancel')"
        >
          Отмена
        </button>
        <button 
          type="submit" 
          class="announcement-form__btn announcement-form__btn--primary"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? 'Сохранение...' : (isEditing ? 'Обновить' : 'Опубликовать') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { Announcement, AnnouncementCategory } from '@/types/announcement'
import { ANNOUNCEMENT_CATEGORIES } from '@/types/announcement'

interface Props {
  announcement?: Announcement
  isEditing?: boolean
}

interface FormData {
  title: string
  content: string
  category: AnnouncementCategory | ''
  images: string[]
  videos: string[]
}

interface FormErrors {
  title?: string
  content?: string
  category?: string
}

const props = withDefaults(defineProps<Props>(), {
  isEditing: false
})

const emit = defineEmits<{
  submit: [data: FormData]
  cancel: []
}>()

// Состояние формы
const form = reactive<FormData>({
  title: props.announcement?.title || '',
  content: props.announcement?.content || '',
  category: props.announcement?.category || '',
  images: props.announcement?.images || [],
  videos: props.announcement?.videos || []
})

// Ошибки валидации
const errors = reactive<FormErrors>({})

// Состояние отправки
const isSubmitting = ref(false)

// Ссылки на input элементы
const imageInput = ref<HTMLInputElement>()
const videoInput = ref<HTMLInputElement>()

// Выбор категории
const selectCategory = (category: AnnouncementCategory) => {
  form.category = category
  if (errors.category) {
    delete errors.category
  }
}

// Валидация формы
const validateForm = (): boolean => {
  errors.title = ''
  errors.content = ''
  errors.category = ''

  if (!form.title.trim()) {
    errors.title = 'Заголовок обязателен'
  } else if (form.title.length < 5) {
    errors.title = 'Заголовок должен содержать минимум 5 символов'
  }

  if (!form.content.trim()) {
    errors.content = 'Содержание обязательно'
  } else if (form.content.length < 10) {
    errors.content = 'Содержание должно содержать минимум 10 символов'
  }

  if (!form.category) {
    errors.category = 'Выберите категорию'
  }

  return !errors.title && !errors.content && !errors.category
}

// Обработка отправки формы
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true
  
  try {
    emit('submit', { ...form })
  } catch (error) {
    console.error('Ошибка при отправке формы:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Загрузка изображений
const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files

  if (files) {
    Array.from(files).forEach(file => {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const result = e.target?.result as string
          if (result && !form.images.includes(result)) {
            form.images.push(result)
          }
        }
        reader.readAsDataURL(file)
      }
    })
  }
}

// Загрузка видео
const handleVideoUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files

  if (files) {
    Array.from(files).forEach(file => {
      if (file.type.startsWith('video/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const result = e.target?.result as string
          if (result && !form.videos.includes(result)) {
            form.videos.push(result)
          }
        }
        reader.readAsDataURL(file)
      }
    })
  }
}

// Удаление изображения
const removeImage = (index: number) => {
  form.images.splice(index, 1)
}

// Удаление видео
const removeVideo = (index: number) => {
  form.videos.splice(index, 1)
}

// Получение имени файла
const getFileName = (url: string): string => {
  // Простая реализация для демонстрации
  return url.split('/').pop() || 'video.mp4'
}
</script>

<style scoped>
.announcement-form {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  max-width: 800px;
  margin: 0 auto;
}

.announcement-form__title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

.announcement-form__form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.announcement-form__field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.announcement-form__label {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

/* Категории */
.announcement-form__category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-sm);
}

.announcement-form__category-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  background: var(--bg-tertiary);
}

.announcement-form__category-option:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.announcement-form__category-option--selected {
  border-color: var(--primary-color);
  background: var(--primary-color);
  color: var(--white);
}

.announcement-form__category-icon {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.announcement-form__category-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  text-align: center;
}

/* Поля ввода */
.announcement-form__input,
.announcement-form__textarea {
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-family: var(--font-family-body);
  font-size: var(--font-size-base);
  transition: border-color var(--duration-fast) var(--ease-in-out);
}

.announcement-form__input:focus,
.announcement-form__textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(162, 155, 254, 0.1);
}

.announcement-form__input--error,
.announcement-form__textarea--error {
  border-color: var(--error-color);
}

.announcement-form__textarea {
  resize: vertical;
  min-height: 120px;
}

.announcement-form__error {
  color: var(--error-color);
  font-size: var(--font-size-sm);
}

.announcement-form__counter {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  text-align: right;
}

/* Загрузка файлов */
.announcement-form__file-upload {
  position: relative;
}

.announcement-form__file-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.announcement-form__file-dropzone {
  border: 2px dashed var(--border-color);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  text-align: center;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
}

.announcement-form__file-dropzone:hover {
  border-color: var(--primary-color);
  background: rgba(162, 155, 254, 0.05);
}

.announcement-form__file-icon {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-sm);
}

.announcement-form__file-text {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

/* Предварительный просмотр изображений */
.announcement-form__images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}

.announcement-form__image-preview {
  position: relative;
  border-radius: var(--border-radius);
  overflow: hidden;
}

.announcement-form__image-preview img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

.announcement-form__image-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--error-color);
  color: var(--white);
  border: none;
  cursor: pointer;
  font-size: var(--font-size-xs);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Список видео */
.announcement-form__videos-list {
  margin-top: var(--spacing-sm);
}

.announcement-form__video-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm);
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-xs);
}

.announcement-form__video-name {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.announcement-form__video-remove {
  background: var(--error-color);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius);
  padding: var(--spacing-xs);
  cursor: pointer;
  font-size: var(--font-size-xs);
}

/* Кнопки действий */
.announcement-form__actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-light);
}

.announcement-form__btn {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  border: none;
}

.announcement-form__btn--primary {
  background: var(--primary-color);
  color: var(--white);
}

.announcement-form__btn--primary:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.announcement-form__btn--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.announcement-form__btn--secondary {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.announcement-form__btn--secondary:hover {
  background: var(--border-color);
  color: var(--text-primary);
}

/* Адаптивность */
@media (max-width: 768px) {
  .announcement-form {
    padding: var(--spacing-lg);
  }

  .announcement-form__category-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }

  .announcement-form__actions {
    flex-direction: column;
  }

  .announcement-form__btn {
    width: 100%;
  }
}
</style> 