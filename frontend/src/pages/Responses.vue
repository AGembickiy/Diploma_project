<template>
  <MainLayout>
    <div class="responses-container">
      <div class="responses-header">
        <div class="responses-stats">
          <span class="stats-item">
            Всего: {{ allResponses.length }}
          </span>
          <span class="stats-item">
            Новые: {{ newResponses.length }}
          </span>
          <span class="stats-item">
            Принятые: {{ acceptedResponses.length }}
          </span>
        </div>
      </div>

      <div class="responses-filters">
        <div class="filter-group">
          <label class="filter-label">Объявление:</label>
          <select v-model="selectedAdvertisement" class="filter-select">
            <option value="all">Все объявления</option>
            <option 
              v-for="ad in userAdvertisements" 
              :key="ad.id" 
              :value="ad.id"
            >
              {{ ad.title }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="filter-label">Статус:</label>
          <select v-model="statusFilter" class="filter-select">
            <option value="all">Все отклики</option>
            <option value="new">Новые</option>
            <option value="accepted">Принятые</option>
            <option value="rejected">Отклоненные</option>
          </select>
        </div>
      </div>

      <div class="responses-list-wrapper">
        <CardList 
          :items="filteredResponses"
          sort-by="date-desc"
          sort-field="created_at"
          empty-icon="💬"
          empty-title="Нет откликов"
          empty-description="У вас пока нет откликов на объявления."
        >
          <template #default="{ item }">
            <ResponseCard
              :response="item"
              @delete="handleDeleteResponse"
              @accept="handleAcceptResponse"
              @reject="handleRejectResponse"
            />
          </template>
        </CardList>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import ResponseCard from '@/components/advertisement/ResponseCard.vue'
import CardList from '@/components/ui/CardList.vue'
// import { useUserStore } from '@/stores/user'
import type { Response, Advertisement } from '@/types/advertisement'

// const _user = useUserStore()

// Фильтры
const selectedAdvertisement = ref<'all' | number>('all')
const statusFilter = ref<'all' | 'new' | 'accepted' | 'rejected'>('all')
// const _sortBy = ref<'date-desc' | 'date-asc' | 'author'>('date-desc')

// Объявления пользователя (пустой массив для реальных данных)
const userAdvertisements = ref<Advertisement[]>([])

// Отклики на объявления пользователя (пустой массив для реальных данных)
const allResponses = ref<Response[]>([])

// Статусы откликов (пустой объект для реальных данных)
const responseStatuses = ref<Record<number, 'new' | 'accepted' | 'rejected'>>({})

// Фильтрация откликов
const filteredResponses = computed(() => {
  let responses = allResponses.value

  // Фильтр по объявлению
  if (selectedAdvertisement.value !== 'all') {
    responses = responses.filter(response => response.advertisementId === selectedAdvertisement.value)
  }

  // Фильтр по статусу
  if (statusFilter.value !== 'all') {
    responses = responses.filter(response => {
      const status = responseStatuses.value[response.id] || 'new'
      return status === statusFilter.value
    })
  }

  return responses
})

// Статистика
const newResponses = computed(() => 
  allResponses.value.filter(response => (responseStatuses.value[response.id] || 'new') === 'new')
)

const acceptedResponses = computed(() => 
  allResponses.value.filter(response => responseStatuses.value[response.id] === 'accepted')
)

// Обработчики
const handleDeleteResponse = (response: Response) => {
  if (confirm('Вы уверены, что хотите удалить этот отклик?')) {
    const index = allResponses.value.findIndex(r => r.id === response.id)
    if (index !== -1) {
      allResponses.value.splice(index, 1)
      delete responseStatuses.value[response.id]
    }
  }
}

const handleAcceptResponse = (response: Response) => {
  responseStatuses.value[response.id] = 'accepted'
  alert(`Отклик от ${response.authorName} принят!`)
}

const handleRejectResponse = (response: Response) => {
  responseStatuses.value[response.id] = 'rejected'
  alert(`Отклик от ${response.authorName} отклонен.`)
}
</script>

<style scoped>
.responses-container {
  width: 100%;
  max-width: 6xl;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.responses-header {
  flex-shrink: 0;
}

.responses-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.stats-item {
  color: var(--text-secondary, #b8b8b8);
  font-size: 12px;
  font-family: var(--font-family-body);
  padding: 4px 12px;
  background: var(--bg-tertiary, #4a4a6a);
  border-radius: 16px;
  border: 1px solid var(--border-color, #4a4a6a);
}

.responses-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  flex-shrink: 0;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  color: var(--text-secondary, #b8b8b8);
  font-size: 12px;
  font-family: var(--font-family-body);
  white-space: nowrap;
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
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-color, #a29bfe);
  box-shadow: 0 0 0 2px rgba(162, 155, 254, 0.2);
}

.responses-list-wrapper {
  flex: 1;
  overflow: hidden;
}

@media (max-width: 768px) {
  .responses-stats {
    gap: 0.5rem;
  }
  
  .stats-item {
    font-size: 10px;
    padding: 3px 8px;
  }
  
  .responses-filters {
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