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
        
        <!-- Индикатор загрузки -->
        <div v-if="isLoading" class="loading-indicator">
          <span class="loading-text">Загрузка...</span>
        </div>
        
        <!-- Сообщение об ошибке -->
        <div v-if="error" class="error-message">
          <span class="error-text">{{ error }}</span>
          <button @click="loadData" class="retry-btn">Повторить</button>
        </div>
        

      </div>

      <div class="responses-filters">
        <div class="filter-group">
          <label class="filter-label">Объявление:</label>
          <select v-model="selectedAdvertisement" class="filter-select" @change="handleFilterChange">
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
          <select v-model="statusFilter" class="filter-select" @change="handleFilterChange">
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

      <ConfirmationDialog
        :isVisible="confirmState.visible"
        :title="confirmState.title"
        :message="confirmState.message"
        :confirmText="confirmState.confirmText"
        :cancelText="confirmState.cancelText"
        :showCancel="true"
        @confirm="confirmState.onConfirm && confirmState.onConfirm()"
        @close="closeConfirm"
      />
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import ResponseCard from '@/components/advertisement/ResponseCard.vue'
import CardList from '@/components/ui/CardList.vue'
import { useUserStore } from '@/stores/user'
import { ResponsesService } from '@/services/responses'
import type { Response, Advertisement } from '@/types/advertisement'
import ConfirmationDialog from '@/components/advertisement/ConfirmationDialog.vue'

const userStore = useUserStore()

// Состояние загрузки
const isLoading = ref(false)
const error = ref<string | null>(null)

// Фильтры
const selectedAdvertisement = ref<'all' | number>('all')
const statusFilter = ref<'all' | 'new' | 'accepted' | 'rejected'>('all')

// Объявления пользователя
const userAdvertisements = ref<Advertisement[]>([])

// Отклики на объявления пользователя
const allResponses = ref<Response[]>([])

// Фильтрация откликов
const filteredResponses = computed(() => {
  let responses = allResponses.value

  // Фильтр по объявлению
  if (selectedAdvertisement.value !== 'all') {
    responses = responses.filter(response => response.advertisement.id === selectedAdvertisement.value)
  }

  // Фильтр по статусу
  if (statusFilter.value !== 'all') {
    responses = responses.filter(response => response.status === statusFilter.value)
  }

  return responses
})

// Статистика
const newResponses = computed(() => 
  allResponses.value.filter(response => response.status === 'new')
)

const acceptedResponses = computed(() => 
  allResponses.value.filter(response => response.status === 'accepted')
)

// Загрузка данных
const loadData = async () => {
  if (!userStore.isAuthenticated) return
  
  isLoading.value = true
  error.value = null
  
  try {
    // Загружаем объявления и отклики параллельно
    const [advertisements, responses] = await Promise.all([
      ResponsesService.getMyAdvertisements(),
      ResponsesService.getMyAdvertisementResponses()
    ])
    
    userAdvertisements.value = advertisements
    allResponses.value = responses.map(response => ({
      ...response,
      // Добавляем совместимые поля для существующего кода
      advertisementId: response.advertisement.id,
      authorName: response.author.username,
      createdAt: new Date(response.created_at)
    }))
    

  } catch (err) {
    console.error('❌ Ошибка загрузки данных:', err)
    error.value = 'Ошибка загрузки данных. Попробуйте обновить страницу.'
  } finally {
    isLoading.value = false
  }
}

// Обновление данных при изменении фильтров
const updateResponses = async () => {
  if (!userStore.isAuthenticated) return
  
  try {
    // Загружаем все данные заново для актуальности
    await loadData()
  } catch (err) {
    console.error('❌ Ошибка обновления откликов:', err)
    error.value = 'Ошибка обновления данных.'
  }
}

// Обработчики
type ConfirmState = {
  visible: boolean
  title: string
  message: string
  confirmText: string
  cancelText: string
  onConfirm: null | (() => void)
}

const confirmState = ref<ConfirmState>({
  visible: false,
  title: 'Подтверждение',
  message: '',
  confirmText: 'Удалить',
  cancelText: 'Отмена',
  onConfirm: null
})

const openConfirm = (cfg: Partial<ConfirmState>) => {
  confirmState.value = {
    visible: true,
    title: cfg.title ?? 'Подтверждение',
    message: cfg.message ?? '',
    confirmText: cfg.confirmText ?? 'Подтвердить',
    cancelText: cfg.cancelText ?? 'Отмена',
    onConfirm: cfg.onConfirm ?? null
  }
}

const closeConfirm = () => {
  confirmState.value.visible = false
  confirmState.value.onConfirm = null
}

const handleDeleteResponse = async (response: Response) => {
  openConfirm({
    title: 'Удалить отклик',
    message: 'Вы уверены, что хотите удалить этот отклик? Это действие необратимо.',
    confirmText: 'Удалить',
    cancelText: 'Отмена',
    onConfirm: async () => {
      try {
        await ResponsesService.deleteResponse(response.id)
        // Автоматически обновляем данные с сервера
        await loadData()
      } catch (err) {
        console.error('❌ Ошибка удаления отклика:', err)
        error.value = 'Ошибка удаления отклика. Попробуйте обновить страницу.'
      }
    }
  })
}

const handleAcceptResponse = async (response: Response) => {
  try {
    await ResponsesService.changeResponseStatus(response.id, 'accepted')
    // Автоматически обновляем данные с сервера
    await loadData()
  } catch (err) {
    console.error('❌ Ошибка принятия отклика:', err)
    error.value = 'Ошибка принятия отклика. Попробуйте обновить страницу.'
  }
}

const handleRejectResponse = async (response: Response) => {
  try {
    await ResponsesService.changeResponseStatus(response.id, 'rejected')
    // Автоматически обновляем данные с сервера
    await loadData()
  } catch (err) {
    console.error('❌ Ошибка отклонения отклика:', err)
    error.value = 'Ошибка отклонения отклика. Попробуйте обновить страницу.'
  }
}

// Наблюдаем за изменениями фильтров
const handleFilterChange = () => {
  updateResponses()
}

// Интервал для автоматического обновления данных
let autoRefreshInterval: number | null = null

// Загружаем данные при монтировании компонента
onMounted(() => {
  loadData()
  
  // Автоматическое обновление данных каждые 30 секунд
  autoRefreshInterval = setInterval(() => {
    if (!isLoading.value) {
      loadData()
    }
  }, 30000) // 30 секунд
})

// Очищаем интервал при размонтировании компонента
onUnmounted(() => {
  if (autoRefreshInterval) {
    clearInterval(autoRefreshInterval)
  }
})
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

.loading-indicator {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.loading-text {
  color: var(--primary-color, #a29bfe);
  font-size: 14px;
  font-family: var(--font-family-body);
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 1rem;
  background: var(--error-color, #e17055);
  border-radius: 8px;
  border: 1px solid var(--error-color, #e17055);
}

.error-text {
  color: #fff;
  font-size: 14px;
  font-family: var(--font-family-body);
  text-align: center;
}

.retry-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-family-body);
}

.retry-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.refresh-section {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.refresh-btn {
  background: var(--primary-color, #a29bfe);
  border: 1px solid var(--primary-color, #a29bfe);
  color: #fff;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-family-body);
}

.refresh-btn:hover:not(:disabled) {
  background: var(--primary-light, #b8a9ff);
  border-color: var(--primary-light, #b8a9ff);
}

.refresh-btn:disabled {
  background: var(--text-muted, #8a8a8a);
  border-color: var(--text-muted, #8a8a8a);
  cursor: not-allowed;
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