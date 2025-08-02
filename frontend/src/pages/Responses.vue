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
          sort-field="createdAt"
          empty-icon="📝"
          empty-title="Нет откликов"
          :empty-description="getEmptyStateMessage()"
          empty-action-link="/board"
          empty-action-text="Создать объявление"
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
import { useUserStore } from '@/stores/user'
import type { Response, Advertisement } from '@/types/advertisement'

const user = useUserStore()

// Фильтры
const selectedAdvertisement = ref<'all' | number>('all')
const statusFilter = ref<'all' | 'new' | 'accepted' | 'rejected'>('all')
const sortBy = ref<'date-desc' | 'date-asc' | 'author'>('date-desc')

// Объявления пользователя (моковые данные)
const userAdvertisements = ref<Advertisement[]>([
  {
    id: 1,
    title: 'Опытный танк ищет гильдию',
    description: 'Танк 80 уровня с полным комплектом эпического снаряжения.',
    category: 'Танки',
    image: '/images/tank.jpg',
    createdAt: new Date('2024-03-20'),
    media: {
      images: ['/images/tank1.jpg', '/images/tank2.jpg'],
      video: true
    }
  },
  {
    id: 2,
    title: 'Гильдмастер набирает команду',
    description: 'Собираю команду для новой гильдии.',
    category: 'Гилдмастеры',
    image: '/images/guild.jpg',
    createdAt: new Date('2024-03-19'),
    media: {
      images: ['/images/guild1.jpg'],
      video: true,
      audio: true
    }
  }
])

// Отклики на объявления пользователя (моковые данные)
const allResponses = ref<Response[]>([
  {
    id: 1,
    advertisementId: 1,
    authorId: 2,
    authorName: 'Игрок_Алекс',
    text: 'Привет! Очень заинтересовало ваше объявление. У меня есть опыт танкования, готов к тестированию.',
    createdAt: new Date('2024-03-21T10:30:00')
  },
  {
    id: 2,
    advertisementId: 1,
    authorId: 3,
    authorName: 'Танк_Макс',
    text: 'Здравствуйте! Я ищу гильдию для рейдов. У меня есть опыт танкования в сложных боях.',
    createdAt: new Date('2024-03-20T15:45:00')
  },
  {
    id: 3,
    advertisementId: 2,
    authorId: 4,
    authorName: 'Хил_Анна',
    text: 'Приветствую! Я опытный хил 85 уровня. Ищу активную гильдию для рейдов.',
    createdAt: new Date('2024-03-19T09:15:00')
  },
  {
    id: 4,
    advertisementId: 2,
    authorId: 5,
    authorName: 'ДД_Сергей',
    text: 'Добрый день! Я ДД 90 уровня, ищу статик для рейдов.',
    createdAt: new Date('2024-03-18T14:20:00')
  }
])

// Статусы откликов (в реальном приложении это будет в базе данных)
const responseStatuses = ref<Record<number, 'new' | 'accepted' | 'rejected'>>({
  1: 'new',
  2: 'accepted',
  3: 'new',
  4: 'rejected'
})

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

const getEmptyStateMessage = () => {
  if (selectedAdvertisement.value !== 'all') {
    return 'На выбранное объявление нет откликов'
  }
  
  if (statusFilter.value !== 'all') {
    return `Нет откликов со статусом "${statusFilter.value}"`
  }
  
  return 'На ваши объявления пока нет откликов'
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