<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">📧 Создать новую рассылку</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          ✕
        </button>
      </div>

      <form @submit.prevent="createNewsletter" class="space-y-4">
        <!-- Заголовок -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Заголовок рассылки *
          </label>
          <input
            v-model="form.title"
            type="text"
            required
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Введите заголовок рассылки"
          />
        </div>

        <!-- Тема письма -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Тема письма *
          </label>
          <input
            v-model="form.subject"
            type="text"
            required
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Введите тему письма"
          />
        </div>

        <!-- Содержание -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Содержание *
          </label>
          <textarea
            v-model="form.content"
            required
            rows="8"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Введите содержание рассылки..."
          ></textarea>
        </div>

        <!-- Тип получателей -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Получатели *
          </label>
          <div class="space-y-2">
            <label class="flex items-center">
              <input
                v-model="form.send_to_all"
                type="radio"
                name="recipients"
                class="mr-2"
                @change="updateRecipients('all')"
              />
              <span>Все пользователи</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="form.send_to_active"
                type="radio"
                name="recipients"
                class="mr-2"
                @change="updateRecipients('active')"
              />
              <span>Только активные пользователи (зарегистрированные более 7 дней назад)</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="form.send_to_new"
                type="radio"
                name="recipients"
                class="mr-2"
                @change="updateRecipients('new')"
              />
              <span>Только новые пользователи (зарегистрированные за последние 7 дней)</span>
            </label>
          </div>
        </div>

        <!-- Запланированная отправка -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Запланированная отправка (необязательно)
          </label>
          <input
            v-model="form.scheduled_at"
            type="datetime-local"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p class="text-sm text-gray-500 mt-1">
            Оставьте пустым для немедленной отправки
          </p>
        </div>

        <!-- Предварительный просмотр -->
        <div v-if="form.subject || form.content">
          <h3 class="text-sm font-medium text-gray-700 mb-2">Предварительный просмотр:</h3>
          <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
            <div class="font-semibold text-gray-800 mb-2">{{ form.subject || 'Тема письма' }}</div>
            <div class="text-gray-600 whitespace-pre-wrap">{{ form.content || 'Содержание письма' }}</div>
          </div>
        </div>

        <!-- Кнопки -->
        <div class="flex justify-end gap-3 pt-4">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Отмена
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {{ loading ? 'Создание...' : 'Создать рассылку' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import newsletterService from '@/services/newsletters';
import type { NewsletterCreate } from '@/types/newsletter';

const emit = defineEmits<{
  close: [];
  created: [];
}>();

const loading = ref(false);

const form = ref<NewsletterCreate>({
  title: '',
  subject: '',
  content: '',
  send_to_all: false,
  send_to_active: false,
  send_to_new: false,
  scheduled_at: undefined
});

const updateRecipients = (type: 'all' | 'active' | 'new') => {
  form.value.send_to_all = type === 'all';
  form.value.send_to_active = type === 'active';
  form.value.send_to_new = type === 'new';
};

const createNewsletter = async () => {
  if (!form.value.title || !form.value.subject || !form.value.content) {
    alert('Пожалуйста, заполните все обязательные поля');
    return;
  }

  if (!form.value.send_to_all && !form.value.send_to_active && !form.value.send_to_new) {
    alert('Пожалуйста, выберите тип получателей');
    return;
  }

  loading.value = true;
  
  try {
    await newsletterService.createNewsletter(form.value);
    emit('created');
    
    // Сброс формы
    form.value = {
      title: '',
      subject: '',
      content: '',
      send_to_all: false,
      send_to_active: false,
      send_to_new: false,
      scheduled_at: undefined
    };
  } catch (error) {
    console.error('Ошибка создания рассылки:', error);
    alert('Ошибка создания рассылки');
  } finally {
    loading.value = false;
  }
};
</script>
