<template>
  <div class="filters-container">
    <div class="filters-content">
      <!-- Фильтр по категориям -->
      <div class="filter-group">
        <label class="filter-label">Категория:</label>
        <select v-model="selectedCategory" @change="applyFilters" class="filter-select">
          <option value="all">Все категории</option>
          <option 
            v-for="category in categories" 
            :key="category" 
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>
      
      <!-- Фильтр по времени -->
      <div class="filter-group">
        <label class="filter-label">Время создания:</label>
        <select v-model="selectedTimeFilter" @change="applyFilters" class="filter-select">
          <option 
            v-for="timeFilter in timeFilters" 
            :key="timeFilter.value" 
            :value="timeFilter.value"
          >
            {{ timeFilter.label }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { AdvertisementCategory } from '@/types/advertisement'

// Пропсы
interface Props {
  modelValue?: {
    category: AdvertisementCategory | 'all'
    timeFilter: string
  }
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => ({
    category: 'all',
    timeFilter: 'all'
  })
})

// Эмиты
const emit = defineEmits<{
  'update:modelValue': [value: { category: AdvertisementCategory | 'all', timeFilter: string }]
}>()

// Категории
const categories: AdvertisementCategory[] = [
  'Танки',
  'Хилы', 
  'ДД',
  'Торговцы',
  'Гилдмастеры',
  'Квестгиверы',
  'Кузнецы',
  'Кожевники',
  'Зельевары',
  'Мастера заклинаний'
]

// Фильтры по времени
const timeFilters = [
  { value: 'all', label: 'Все время' },
  { value: '1d', label: 'За сутки' },
  { value: '3d', label: 'За трое суток' },
  { value: '7d', label: 'За неделю' }
]

// Локальное состояние
const selectedCategory = ref<AdvertisementCategory | 'all'>(props.modelValue.category)
const selectedTimeFilter = ref<string>(props.modelValue.timeFilter)

// Вычисляемое свойство для проверки активных фильтров
// const _hasActiveFilters = computed(() => {
//   return selectedCategory.value !== 'all' || selectedTimeFilter.value !== 'all'
// })

// Применение фильтров
const applyFilters = () => {
  emit('update:modelValue', {
    category: selectedCategory.value,
    timeFilter: selectedTimeFilter.value
  })
}

// Синхронизация с внешними изменениями
watch(() => props.modelValue, (newValue) => {
  selectedCategory.value = newValue.category
  selectedTimeFilter.value = newValue.timeFilter
}, { deep: true })
</script>

<style scoped>
.filters-container {
  margin-bottom: var(--spacing-md);
}

.filters-content {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  align-items: baseline;
  flex-shrink: 0;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1;
}

.filter-label {
  color: var(--text-secondary, #b8b8b8);
  font-size: 12px;
  font-family: var(--font-family-body);
  white-space: nowrap;
  line-height: 1;
}

.filter-select {
  background: var(--bg-tertiary, #4a4a6a);
  border: 1px solid var(--border-color, #4a4a6a);
  color: var(--text-primary, #fff);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-family: var(--font-family-body);
  cursor: pointer;
  transition: all 0.2s;
  min-width: 180px;
  line-height: 1;
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-color, #a29bfe);
  box-shadow: 0 0 0 2px rgba(162, 155, 254, 0.2);
}

@media (max-width: 768px) {
  .filters-content {
    flex-direction: column;
    align-items: center;
  }
  
  .filter-group {
    width: 100%;
    max-width: 250px;
  }
  
  .filter-select {
    min-width: auto;
    width: 100%;
  }
}
</style> 