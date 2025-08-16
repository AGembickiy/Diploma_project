<template>
  <MainLayout>
    <div class="main-container">
      <!-- Фильтры и результаты в одной строке -->
      <div class="filters-and-results">
        <AdvertisementFilters 
          v-model="filters"
          @update:modelValue="applyFilters"
        />
        
        <!-- Результаты фильтрации -->
        <div class="results-info">
          <span class="results-count">{{ filteredAdvertisements.length }}</span>
          <span class="results-text">объявлений</span>
        </div>
      </div>
      
      <!-- Активные фильтры -->
      <div v-if="hasActiveFilters" class="active-filters">
        <span class="active-filters-label">Активные фильтры:</span>
        <div class="filter-tags">
          <span 
            v-if="filters.category !== 'all'"
            class="filter-tag category-tag"
          >
            {{ filters.category }}
          </span>
          <span 
            v-if="filters.timeFilter !== 'all'"
            class="filter-tag time-tag"
          >
            {{ getTimeFilterLabel(filters.timeFilter) }}
          </span>
        </div>
      </div>
      
      <div class="ad-list-wrapper">
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Загрузка объявлений...</p>
        </div>
        
        <CardList 
          v-else
          :items="filteredAdvertisements"
          sort-by="date-desc"
          sort-field="created_at"
          empty-icon="🔍"
          empty-title="Ничего не найдено"
          empty-description="У вас нет созданных объявлений."
        >
          <template #default="{ item }">
            <AdvertisementCard
              :advertisement="item"
              @response="handleResponse"
            />
          </template>
        </CardList>
      </div>
    </div>
    
    <ResponseDialog 
      :is-visible="isResponseDialogVisible"
      :advertisement="selectedAdvertisement"
      @close="closeResponseDialog"
      @submit="handleResponseSubmit"
    />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import AdvertisementCard from '@/components/advertisement/AdvertisementCard.vue'
import AdvertisementFilters from '@/components/advertisement/AdvertisementFilters.vue'
import ResponseDialog from '@/components/advertisement/ResponseDialog.vue'
import CardList from '@/components/ui/CardList.vue'
import { useUserStore } from '@/stores/user'
import type { Advertisement, AdvertisementCategory } from '@/types/advertisement'
import axios from 'axios'

const user = useUserStore()

// Состояние фильтров
const filters = ref({
  category: 'all' as AdvertisementCategory | 'all',
  timeFilter: 'all' as string
})

// Все объявления (загружаем с API)
const allAdvertisements = ref<Advertisement[]>([])
const isLoading = ref(false)

// Загрузка всех публичных объявлений
const loadPublicAdvertisements = async () => {
  try {
    isLoading.value = true
    console.log('🔄 Загружаю публичные объявления...')
    const response = await axios.get('http://localhost:8000/api/advertisements/public_advertisements/')
    console.log('📡 Ответ API:', response.data)
    allAdvertisements.value = response.data
    console.log('💾 Сохранено объявлений:', allAdvertisements.value.length)
  } catch (error) {
    console.error('❌ Ошибка загрузки объявлений:', error)
    allAdvertisements.value = []
  } finally {
    isLoading.value = false
  }
}

// Загрузка при монтировании компонента
onMounted(() => {
  loadPublicAdvertisements()
})

// Фильтрация объявлений
const filteredAdvertisements = computed(() => {
  console.log('🔍 Фильтрация объявлений. Всего:', allAdvertisements.value.length)
  let filtered = allAdvertisements.value

  // Фильтр по категории
  if (filters.value.category !== 'all') {
    filtered = filtered.filter(ad => ad.category === filters.value.category)
    console.log('📂 После фильтра по категории:', filtered.length)
  }

  // Фильтр по времени
  if (filters.value.timeFilter !== 'all') {
    const now = new Date()
    const timeFilter = filters.value.timeFilter
    
    let timeLimit: Date
    switch (timeFilter) {
      case '1d':
        timeLimit = new Date(now.getTime() - 24 * 60 * 60 * 1000)
        break
      case '3d':
        timeLimit = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000)
        break
      case '7d':
        timeLimit = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
        break
      default:
        timeLimit = new Date(0)
    }
    
    filtered = filtered.filter(ad => new Date(ad.created_at) >= timeLimit)
    console.log('⏰ После фильтра по времени:', filtered.length)
  }

  console.log('✅ Итоговое количество объявлений:', filtered.length)
  return filtered
})

// Проверка активных фильтров
const hasActiveFilters = computed(() => {
  return filters.value.category !== 'all' || filters.value.timeFilter !== 'all'
})

// Получение метки для фильтра времени
const getTimeFilterLabel = (timeFilter: string): string => {
  const labels: Record<string, string> = {
    '1d': 'За сутки',
    '3d': 'За трое суток', 
    '7d': 'За неделю'
  }
  return labels[timeFilter] || ''
}

// Применение фильтров
const applyFilters = (newFilters: { category: AdvertisementCategory | 'all', timeFilter: string }) => {
  filters.value = newFilters
}

// Состояние диалога отклика
const isResponseDialogVisible = ref(false)
const selectedAdvertisement = ref<Advertisement | null>(null)

const handleResponse = (advertisement: Advertisement) => {
  selectedAdvertisement.value = advertisement
  isResponseDialogVisible.value = true
}

const closeResponseDialog = () => {
  isResponseDialogVisible.value = false
  selectedAdvertisement.value = null
}

const handleResponseSubmit = (_response: { advertisementId: number; text: string }) => {
  // Здесь будет отправка отклика на сервер
  
  // Показываем уведомление об успешной отправке
  alert(`Отклик успешно отправлен на объявление "${selectedAdvertisement.value?.title}"`)
}
</script>

<style scoped>
.main-container {
  width: 100%;
  max-width: 6xl;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.filters-and-results {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: var(--spacing-md);
  gap: var(--spacing-md);
}

.results-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-shrink: 0;
  height: 100%;
  line-height: 1;
  white-space: nowrap;
}

.results-count {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-lg);
  font-weight: bold;
  color: var(--primary-color);
  line-height: 1;
}

.results-text {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1;
}

.active-filters {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-light);
}

.active-filters-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.filter-tags {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.filter-tag {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.category-tag {
  background: var(--primary-color);
  color: white;
}

.time-tag {
  background: var(--secondary-color);
  color: white;
}

.ad-list-wrapper {
  flex: 1;
  overflow: hidden;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  text-align: center;
}

.loading-spinner {
  border: 4px solid var(--border-light);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .filters-and-results {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  
  .active-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}

@media (max-width: 900px) {
  .main-body {
    flex-direction: column;
  }
  :deep(.sidebar) {
    width: 100% !important;
    height: auto !important;
    position: relative !important;
  }
}
</style> 