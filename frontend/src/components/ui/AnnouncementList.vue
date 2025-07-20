<template>
  <div class="w-full">
    <div v-if="filteredAnnouncements.length === 0" class="flex flex-col items-center justify-center py-12">
      <div class="text-4xl mb-2">📋</div>
      <h3 class="text-xl font-bold mb-2">Объявлений не найдено</h3>
      <p class="text-base text-muted mb-4">
        {{ selectedCategory 
          ? `В категории "${getCategoryLabel(selectedCategory)}" пока нет объявлений` 
          : 'Пока нет объявлений. Будьте первым!' 
        }}
      </p>
      <button 
        class="px-6 py-3 rounded bg-primary text-white font-medium transition hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
        @click="showCreateForm = true"
        aria-label="Создать первое объявление"
        tabindex="0"
      >
        Создать первое объявление
      </button>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <AnnouncementCard
        v-for="announcement in filteredAnnouncements"
        :key="announcement.id"
        :announcement="announcement"
        @click="selectAnnouncement(announcement)"
      />
    </div>
    <!-- Модальное окно создания/редактирования -->
    <div v-if="showCreateForm || showEditForm" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="absolute inset-0" @click="closeModal" aria-label="Закрыть модальное окно" tabindex="0"></div>
      <div class="relative bg-background rounded-lg shadow-lg p-6 max-w-lg w-full z-10">
        <button 
          class="absolute top-2 right-2 text-xl text-muted hover:text-error focus:outline-none focus:ring-2 focus:ring-error rounded"
          @click="closeModal"
          aria-label="Закрыть"
          tabindex="0"
        >
          ✕
        </button>
        <AnnouncementForm
          :announcement="editingAnnouncement"
          :is-editing="showEditForm"
          @submit="handleFormSubmit"
          @cancel="closeModal"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Announcement, AnnouncementCategory } from '@/types/announcement'
import { ANNOUNCEMENT_CATEGORIES } from '@/types/announcement'
import AnnouncementCard from './AnnouncementCard.vue'
import AnnouncementForm from './AnnouncementForm.vue'

interface Props {
  announcements: Announcement[]
}

const props = defineProps<Props>()

// Состояние фильтров и сортировки
const selectedCategory = ref<AnnouncementCategory | ''>('')
const sortBy = ref<'newest' | 'oldest' | 'title' | 'author'>('newest')

// Состояние модальных окон
const showCreateForm = ref(false)
const showEditForm = ref(false)
const editingAnnouncement = ref<Announcement | undefined>()

// Получение метки категории
const getCategoryLabel = (category: AnnouncementCategory): string => {
  const categoryInfo = ANNOUNCEMENT_CATEGORIES.find(cat => cat.value === category)
  return categoryInfo?.label || category
}

// Фильтрация и сортировка объявлений
const filteredAnnouncements = computed(() => {
  let filtered = props.announcements
  if (selectedCategory.value) {
    filtered = filtered.filter(announcement => announcement.category === selectedCategory.value)
  }
  filtered = [...filtered].sort((a, b) => {
    switch (sortBy.value) {
      case 'newest':
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      case 'oldest':
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      case 'title':
        return a.title.localeCompare(b.title, 'ru')
      case 'author':
        return a.author.localeCompare(b.author, 'ru')
      default:
        return 0
    }
  })
  return filtered
})

const selectAnnouncement = (announcement: Announcement) => {
  editingAnnouncement.value = announcement
  showEditForm.value = true
}

function closeModal() {
  showCreateForm.value = false
  showEditForm.value = false
  editingAnnouncement.value = undefined
}

function handleFormSubmit() {
  closeModal()
}
</script>

<style scoped>
.announcement-list {
  padding: var(--spacing-lg);
}

/* Заголовок и контролы */
.announcement-list__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.announcement-list__title-section {
  flex: 1;
  min-width: 300px;
}

.announcement-list__title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.announcement-list__subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-base);
}

.announcement-list__controls {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  flex-wrap: wrap;
}

.announcement-list__filter {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.announcement-list__filter-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
}

.announcement-list__filter-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: border-color var(--duration-fast) var(--ease-in-out);
}

.announcement-list__filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.announcement-list__create-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--primary-color);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
}

.announcement-list__create-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

/* Контент */
.announcement-list__content {
  min-height: 400px;
}

.announcement-list__grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Пустое состояние */
.announcement-list__empty {
  text-align: center;
  padding: var(--spacing-3xl) var(--spacing-lg);
  color: var(--text-secondary);
}

.announcement-list__empty-icon {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--spacing-lg);
}

.announcement-list__empty-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.announcement-list__empty-text {
  font-size: var(--font-size-base);
  margin-bottom: var(--spacing-lg);
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.announcement-list__empty-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--primary-color);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
}

.announcement-list__empty-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

/* Модальное окно */
.announcement-list__modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
}

.announcement-list__modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.announcement-list__modal-content {
  position: relative;
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

.announcement-list__modal-close {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: none;
  cursor: pointer;
  font-size: var(--font-size-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast) var(--ease-in-out);
  z-index: 1;
}

.announcement-list__modal-close:hover {
  background: var(--error-color);
  color: var(--white);
}

/* Адаптивность */
@media (max-width: 768px) {
  .announcement-list {
    padding: var(--spacing-md);
  }

  .announcement-list__header {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .announcement-list__controls {
    width: 100%;
    justify-content: space-between;
  }

  .announcement-list__filter {
    flex: 1;
  }

  .announcement-list__create-btn {
    width: auto;
  }

  .announcement-list__modal {
    padding: var(--spacing-sm);
  }

  .announcement-list__modal-content {
    max-height: 95vh;
  }
}

@media (max-width: 480px) {
  .announcement-list__controls {
    flex-direction: column;
    align-items: stretch;
  }

  .announcement-list__filter {
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .announcement-list__filter-label {
    min-width: 80px;
  }
}
</style> 