<template>
  <MainLayout>
    <template #header>
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-800">📧 Новостные рассылки</h1>
        <div class="flex gap-2">
          <button
            @click="showCreateDialog = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
          >
            <span>➕</span>
            Создать рассылку
          </button>
          <button
            @click="showTemplateDialog = true"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
          >
            <span>📝</span>
            Шаблоны
          </button>
        </div>
      </div>
    </template>

    <template #content>
      <!-- Статистика -->
      <div class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-2xl font-bold text-blue-600">{{ stats.total_newsletters }}</div>
            <div class="text-gray-600">Всего рассылок</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-2xl font-bold text-green-600">{{ stats.sent_count }}</div>
            <div class="text-gray-600">Отправлено</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-2xl font-bold text-yellow-600">{{ stats.draft_count }}</div>
            <div class="text-gray-600">Черновики</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-2xl font-bold text-purple-600">{{ stats.success_rate.toFixed(1) }}%</div>
            <div class="text-gray-600">Успешность</div>
          </div>
        </div>
      </div>

      <!-- Фильтры -->
      <div class="mb-6 bg-white p-4 rounded-lg shadow">
        <div class="flex flex-wrap gap-4 items-center">
          <select v-model="statusFilter" class="border rounded-lg px-3 py-2">
            <option value="">Все статусы</option>
            <option value="draft">Черновики</option>
            <option value="sending">Отправляется</option>
            <option value="sent">Отправлено</option>
            <option value="cancelled">Отменено</option>
          </select>
          
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск по названию..."
            class="border rounded-lg px-3 py-2 flex-1"
          />
          
          <button
            @click="loadNewsletters"
            class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
          >
            🔄 Обновить
          </button>
        </div>
      </div>

      <!-- Список рассылок -->
      <div class="space-y-4">
        <!-- Простая проверка -->
        <div class="bg-red-100 p-4 rounded-lg">
          <p>Количество рассылок: {{ filteredNewsletters.length }}</p>
          <p>Первая рассылка: {{ filteredNewsletters[0]?.title || 'Нет данных' }}</p>
        </div>
        
        <div
          v-for="newsletter in filteredNewsletters"
          :key="newsletter.id"
          class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h3 class="text-xl font-semibold text-gray-800">{{ newsletter.title }}</h3>
                <span
                  :class="getStatusClass(newsletter.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium"
                >
                  {{ newsletter.status_display }}
                </span>
              </div>
              
              <p class="text-gray-600 mb-2">{{ newsletter.subject }}</p>
              <p class="text-gray-500 text-sm mb-4 line-clamp-2">{{ newsletter.content }}</p>
              
              <div class="flex items-center gap-6 text-sm text-gray-500">
                <span>👤 {{ newsletter.created_by.username }}</span>
                <span>📅 {{ formatDate(newsletter.created_at) }}</span>
                <span>📊 {{ newsletter.total_recipients }} получателей</span>
                <span v-if="newsletter.sent_count > 0">✅ {{ newsletter.sent_count }} отправлено</span>
                <span v-if="newsletter.failed_count > 0">❌ {{ newsletter.failed_count }} ошибок</span>
              </div>
            </div>
            
            <div class="flex flex-col gap-2 ml-4">
              <button
                @click="previewNewsletter(newsletter.id)"
                class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
              >
                👁️ Просмотр
              </button>
              
              <button
                v-if="newsletter.status === 'draft'"
                @click="sendNewsletter(newsletter.id)"
                class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
              >
                📤 Отправить
              </button>
              
              <button
                v-if="newsletter.status === 'draft'"
                @click="duplicateNewsletter(newsletter.id)"
                class="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1 rounded text-sm"
              >
                📋 Дублировать
              </button>
              
              <button
                v-if="['draft', 'sending'].includes(newsletter.status)"
                @click="cancelNewsletter(newsletter.id)"
                class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
              >
                ❌ Отменить
              </button>
              
              <button
                @click="deleteNewsletter(newsletter.id)"
                class="bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded text-sm"
              >
                🗑️ Удалить
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Сообщение об отсутствии рассылок -->
      <div v-if="filteredNewsletters.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">📧</div>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">Рассылки не найдены</h3>
        <p class="text-gray-500">Создайте первую рассылку или измените фильтры</p>
      </div>
    </template>
  </MainLayout>

  <!-- Диалог создания рассылки -->
  <CreateNewsletterDialog
    v-if="showCreateDialog"
    @close="showCreateDialog = false"
    @created="onNewsletterCreated"
  />

  <!-- Диалог шаблонов -->
  <TemplateDialog
    v-if="showTemplateDialog"
    @close="showTemplateDialog = false"
    @template-selected="onTemplateSelected"
  />

  <!-- Диалог предварительного просмотра -->
  <PreviewDialog
    v-if="showPreviewDialog"
    :newsletter="selectedNewsletter"
    @close="showPreviewDialog = false"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import MainLayout from '@/components/layout/MainLayout.vue';
import CreateNewsletterDialog from '@/components/newsletter/CreateNewsletterDialog.vue';
import TemplateDialog from '@/components/newsletter/TemplateDialog.vue';
import PreviewDialog from '@/components/newsletter/PreviewDialog.vue';
import newsletterService from '@/services/newsletters';
import type { Newsletter, NewsletterStats } from '@/types/newsletter';

// Состояние
const newsletters = ref<Newsletter[]>([]);
const stats = ref<NewsletterStats>({
  total_newsletters: 0,
  draft_count: 0,
  sending_count: 0,
  sent_count: 0,
  cancelled_count: 0,
  total_recipients: 0,
  total_sent: 0,
  total_failed: 0,
  success_rate: 0
});

// Фильтры
const statusFilter = ref('');
const searchQuery = ref('');

// Диалоги
const showCreateDialog = ref(false);
const showTemplateDialog = ref(false);
const showPreviewDialog = ref(false);
const selectedNewsletter = ref<Newsletter | null>(null);

// Вычисляемые свойства
const filteredNewsletters = computed(() => {
  console.log('Фильтрация рассылок...');
  console.log('Исходные рассылки:', newsletters.value);
  console.log('Фильтр статуса:', statusFilter.value);
  console.log('Поисковый запрос:', searchQuery.value);
  
  let filtered = newsletters.value;

  if (statusFilter.value) {
    filtered = filtered.filter(n => n.status === statusFilter.value);
    console.log('После фильтра статуса:', filtered);
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(n => 
      n.title.toLowerCase().includes(query) ||
      n.subject.toLowerCase().includes(query) ||
      n.content.toLowerCase().includes(query)
    );
    console.log('После поиска:', filtered);
  }

  console.log('Итоговые отфильтрованные:', filtered);
  return filtered;
});

// Методы
const loadNewsletters = async () => {
  try {
    console.log('Загружаю рассылки...');
    const data = await newsletterService.getNewsletters();
    console.log('Полученные данные:', data);
    newsletters.value = data;
    console.log('Рассылки после установки:', newsletters.value);
  } catch (error) {
    console.error('Ошибка загрузки рассылок:', error);
  }
};

const loadStats = async () => {
  try {
    stats.value = await newsletterService.getNewsletterStats();
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error);
  }
};

const sendNewsletter = async (id: number) => {
  try {
    await newsletterService.sendNewsletter(id);
    await loadNewsletters();
    await loadStats();
  } catch (error) {
    console.error('Ошибка отправки рассылки:', error);
  }
};

const cancelNewsletter = async (id: number) => {
  try {
    await newsletterService.cancelNewsletter(id);
    await loadNewsletters();
    await loadStats();
  } catch (error) {
    console.error('Ошибка отмены рассылки:', error);
  }
};

const duplicateNewsletter = async (id: number) => {
  try {
    await newsletterService.duplicateNewsletter(id);
    await loadNewsletters();
    await loadStats();
  } catch (error) {
    console.error('Ошибка дублирования рассылки:', error);
  }
};

const deleteNewsletter = async (id: number) => {
  if (!confirm('Вы уверены, что хотите удалить эту рассылку?')) return;
  
  try {
    await newsletterService.deleteNewsletter(id);
    await loadNewsletters();
    await loadStats();
  } catch (error) {
    console.error('Ошибка удаления рассылки:', error);
  }
};

const previewNewsletter = async (id: number) => {
  try {
    const newsletter = await newsletterService.getNewsletter(id);
    selectedNewsletter.value = newsletter;
    showPreviewDialog.value = true;
  } catch (error) {
    console.error('Ошибка загрузки рассылки:', error);
  }
};

const onNewsletterCreated = () => {
  showCreateDialog.value = false;
  loadNewsletters();
  loadStats();
};

const onTemplateSelected = () => {
  showTemplateDialog.value = false;
  loadNewsletters();
  loadStats();
};

const getStatusClass = (status: string) => {
  const classes = {
    draft: 'bg-yellow-100 text-yellow-800',
    sending: 'bg-blue-100 text-blue-800',
    sent: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  };
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800';
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU');
};

// Инициализация
onMounted(() => {
  loadNewsletters();
  loadStats();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
