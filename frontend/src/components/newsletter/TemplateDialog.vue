<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">📝 Шаблоны рассылок</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          ✕
        </button>
      </div>

      <!-- Список шаблонов -->
      <div class="space-y-4">
        <div
          v-for="template in templates"
          :key="template.id"
          class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h3 class="text-lg font-semibold text-gray-800">{{ template.name }}</h3>
                <span
                  v-if="template.is_active"
                  class="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs"
                >
                  Активен
                </span>
              </div>
              
              <p class="text-gray-600 mb-2 font-medium">{{ template.subject }}</p>
              <p class="text-gray-500 text-sm line-clamp-3">{{ template.content }}</p>
              
              <div class="text-xs text-gray-400 mt-2">
                Создан: {{ formatDate(template.created_at) }}
              </div>
            </div>
            
            <div class="flex flex-col gap-2 ml-4">
              <button
                @click="useTemplate(template.id)"
                :disabled="loading"
                class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
              >
                {{ loading ? 'Создание...' : 'Использовать' }}
              </button>
              
              <button
                @click="previewTemplate(template)"
                class="bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded text-sm"
              >
                Просмотр
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Сообщение об отсутствии шаблонов -->
      <div v-if="templates.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">📝</div>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">Шаблоны не найдены</h3>
        <p class="text-gray-500">Создайте первый шаблон в админке</p>
      </div>
    </div>
  </div>

  <!-- Диалог предварительного просмотра шаблона -->
  <div v-if="showPreview" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">👁️ Предварительный просмотр</h2>
        <button @click="showPreview = false" class="text-gray-500 hover:text-gray-700">
          ✕
        </button>
      </div>

      <div v-if="selectedTemplate" class="space-y-4">
        <div>
          <h3 class="font-semibold text-gray-800 mb-2">Название:</h3>
          <p class="text-gray-600">{{ selectedTemplate.name }}</p>
        </div>
        
        <div>
          <h3 class="font-semibold text-gray-800 mb-2">Тема:</h3>
          <p class="text-gray-600">{{ selectedTemplate.subject }}</p>
        </div>
        
        <div>
          <h3 class="font-semibold text-gray-800 mb-2">Содержание:</h3>
          <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
            <div class="whitespace-pre-wrap text-gray-600">{{ selectedTemplate.content }}</div>
          </div>
        </div>
      </div>

      <div class="flex justify-end pt-4">
        <button
          @click="showPreview = false"
          class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import newsletterService from '@/services/newsletters';
import type { NewsletterTemplate } from '@/types/newsletter';

const emit = defineEmits<{
  close: [];
  templateSelected: [];
}>();

const templates = ref<NewsletterTemplate[]>([]);
const loading = ref(false);
const showPreview = ref(false);
const selectedTemplate = ref<NewsletterTemplate | null>(null);

const loadTemplates = async () => {
  try {
    templates.value = await newsletterService.getTemplates();
  } catch (error) {
    console.error('Ошибка загрузки шаблонов:', error);
  }
};

const useTemplate = async (templateId: number) => {
  loading.value = true;
  
  try {
    await newsletterService.useTemplate(templateId);
    emit('templateSelected');
  } catch (error) {
    console.error('Ошибка использования шаблона:', error);
    alert('Ошибка создания рассылки из шаблона');
  } finally {
    loading.value = false;
  }
};

const previewTemplate = (template: NewsletterTemplate) => {
  selectedTemplate.value = template;
  showPreview.value = true;
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU');
};

onMounted(() => {
  loadTemplates();
});
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
