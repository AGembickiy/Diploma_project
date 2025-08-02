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
        <CardList 
          :items="filteredAdvertisements"
          sort-by="date-desc"
          sort-field="createdAt"
          empty-icon="🔍"
          empty-title="Ничего не найдено"
          empty-description="Попробуйте изменить фильтры или создать новое объявление."
          empty-action-link="/board"
          empty-action-text="Создать объявление"
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
import { ref, computed } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import AdvertisementCard from '@/components/advertisement/AdvertisementCard.vue'
import AdvertisementFilters from '@/components/advertisement/AdvertisementFilters.vue'
import ResponseDialog from '@/components/advertisement/ResponseDialog.vue'
import CardList from '@/components/ui/CardList.vue'
import { useUserStore } from '@/stores/user'
import type { Advertisement, AdvertisementCategory } from '@/types/advertisement'

const user = useUserStore()

// Состояние фильтров
const filters = ref({
  category: 'all' as AdvertisementCategory | 'all',
  timeFilter: 'all' as string
})

// Все объявления (включая пользовательские)
const allAdvertisements = ref<Advertisement[]>([
  {
    id: 1,
    title: 'Опытный танк ищет гильдию',
    description: 'Танк 80 уровня с полным комплектом эпического снаряжения. Есть опыт всех рейдов. Готов к долгосрочному сотрудничеству.',
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
    description: 'Собираю команду для новой гильдии. Нужны активные игроки всех классов. Есть свой Discord сервер.',
    category: 'Гилдмастеры',
    image: '/images/guild.jpg',
    createdAt: new Date('2024-03-19'),
    media: {
      images: ['/images/guild1.jpg'],
      video: true,
      audio: true
    }
  },
  {
    id: 3,
    title: 'Зельевар ищет заказы',
    description: 'Варю все виды зелий. Большой опыт, лучшие ингредиенты. Оптовые заказы приветствуются.',
    category: 'Зельевары',
    image: '/images/potion.jpg',
    createdAt: new Date('2024-03-18'),
    media: {
      images: ['/images/potion1.jpg', '/images/potion2.jpg', '/images/potion3.jpg']
    }
  },
  {
    id: 4,
    title: 'Хил ищет статик',
    description: 'Опытный хил 85 уровня. Ищу статик для рейдов. Есть опыт всех контентов.',
    category: 'Хилы',
    image: '/images/healer.jpg',
    createdAt: new Date('2024-03-17'),
    media: {
      images: ['/images/healer1.jpg'],
      video: true
    }
  },
  {
    id: 5,
    title: 'ДД на заказы',
    description: 'ДД 90 уровня. Готов на любые заказы. Быстро и качественно.',
    category: 'ДД',
    image: '/images/dd.jpg',
    createdAt: new Date('2024-03-16'),
    media: {
      images: ['/images/dd1.jpg', '/images/dd2.jpg']
    }
  },
  {
    id: 6,
    title: 'Кузнец принимает заказы',
    description: 'Кузнец 95 уровня. Делаю оружие и броню любой сложности. Гарантия качества.',
    category: 'Кузнецы',
    image: '/images/blacksmith.jpg',
    createdAt: new Date('2024-03-15'),
    media: {
      images: ['/images/blacksmith1.jpg']
    }
  },
  {
    id: 7,
    title: 'Торговец редкими товарами',
    description: 'Продаю редкие материалы и артефакты. Постоянные клиенты получают скидки.',
    category: 'Торговцы',
    image: '/images/merchant.jpg',
    createdAt: new Date('2024-03-14'),
    media: {
      images: ['/images/merchant1.jpg', '/images/merchant2.jpg']
    }
  }
])

// Фильтрация объявлений
const filteredAdvertisements = computed(() => {
  let filtered = allAdvertisements.value

  // Фильтр по пользователю (исключаем объявления текущего пользователя)
  if (!user.isGuest) {
    filtered = filtered.slice(2) // Пока используем простую логику
  }

  // Фильтр по категории
  if (filters.value.category !== 'all') {
    filtered = filtered.filter(ad => ad.category === filters.value.category)
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
    
    filtered = filtered.filter(ad => ad.createdAt >= timeLimit)
  }

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

const handleResponseSubmit = (response: { advertisementId: number; text: string }) => {
  // Здесь будет отправка отклика на сервер
  console.log('Отправка отклика:', response)
  
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