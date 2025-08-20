<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">👁️ Предварительный просмотр рассылки</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          ✕
        </button>
      </div>

      <div v-if="newsletter" class="space-y-6">
        <!-- Основная информация -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="font-semibold text-gray-800 mb-2">Основная информация:</h3>
            <div class="space-y-2 text-sm">
              <div><span class="font-medium">Заголовок:</span> {{ newsletter.title }}</div>
              <div><span class="font-medium">Тема:</span> {{ newsletter.subject }}</div>
              <div><span class="font-medium">Статус:</span> 
                <span :class="getStatusClass(newsletter.status)" class="px-2 py-1 rounded-full text-xs">
                  {{ newsletter.status_display }}
                </span>
              </div>
              <div><span class="font-medium">Создатель:</span> {{ newsletter.created_by.username }}</div>
              <div><span class="font-medium">Дата создания:</span> {{ formatDate(newsletter.created_at) }}</div>
              <div v-if="newsletter.sent_at">
                <span class="font-medium">Дата отправки:</span> {{ formatDate(newsletter.sent_at) }}
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-800 mb-2">Настройки отправки:</h3>
            <div class="space-y-2 text-sm">
              <div v-if="newsletter.send_to_all" class="text-green-600">✅ Отправить всем пользователям</div>
              <div v-if="newsletter.send_to_active" class="text-blue-600">✅ Отправить только активным пользователям</div>
              <div v-if="newsletter.send_to_new" class="text-purple-600">✅ Отправить только новым пользователям</div>
              <div><span class="font-medium">Получателей:</span> {{ newsletter.total_recipients }}</div>
              <div v-if="newsletter.sent_count > 0">
                <span class="font-medium">Отправлено:</span> {{ newsletter.sent_count }}
              </div>
              <div v-if="newsletter.failed_count > 0">
                <span class="font-medium">Ошибок:</span> {{ newsletter.failed_count }}
              </div>
            </div>
          </div>
        </div>

        <!-- Содержание -->
        <div>
          <h3 class="font-semibold text-gray-800 mb-2">Содержание рассылки:</h3>
          <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
            <div class="whitespace-pre-wrap text-gray-600">{{ newsletter.content }}</div>
          </div>
        </div>

        <!-- Предварительный просмотр email -->
        <div>
          <h3 class="font-semibold text-gray-800 mb-2">Предварительный просмотр email:</h3>
          <div class="border border-gray-300 rounded-lg overflow-hidden">
            <div class="bg-gray-100 px-4 py-2 border-b">
              <div class="text-sm text-gray-600">От: MMORPG Board &lt;noreply@mmorpg-board.ru&gt;</div>
              <div class="text-sm text-gray-600">Кому: Пользователи MMORPG Board</div>
              <div class="text-sm text-gray-600">Тема: {{ newsletter.subject }}</div>
            </div>
            <div class="p-4 bg-white">
              <div class="text-center mb-4">
                <div class="text-2xl font-bold text-red-600 mb-2">🎮 MMORPG Board</div>
                <div class="text-xl text-gray-800">{{ newsletter.title }}</div>
              </div>
              
              <div class="mb-4">
                <p class="text-gray-700">Здравствуйте, пользователь!</p>
              </div>
              
              <div class="bg-gray-50 p-4 rounded-lg mb-4">
                <div class="whitespace-pre-wrap text-gray-700">{{ newsletter.content }}</div>
              </div>
              
              <div class="text-center text-sm text-gray-500 border-t pt-4">
                <p>Это письмо отправлено с сайта MMORPG Board</p>
                <p class="mt-2">
                  <a href="#" class="text-red-600 hover:underline">Отписаться от рассылки</a>
                </p>
                <p class="mt-2">© 2024 MMORPG Board. Все права защищены.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Получатели -->
        <div v-if="newsletter.recipients_count > 0">
          <h3 class="font-semibold text-gray-800 mb-2">Получатели ({{ newsletter.recipients_count }}):</h3>
          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="text-sm text-gray-600">
              <div v-if="newsletter.send_to_all">📧 Все активные пользователи системы</div>
              <div v-else-if="newsletter.send_to_active">📧 Пользователи, зарегистрированные более 7 дней назад</div>
              <div v-else-if="newsletter.send_to_new">📧 Новые пользователи, зарегистрированные за последние 7 дней</div>
            </div>
          </div>
        </div>

        <!-- Действия -->
        <div class="flex justify-end gap-3 pt-4 border-t">
          <button
            @click="$emit('close')"
            class="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Закрыть
          </button>
          
          <button
            v-if="newsletter.status === 'draft'"
            @click="sendNewsletter"
            :disabled="loading"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {{ loading ? 'Отправка...' : '📤 Отправить рассылку' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import newsletterService from '@/services/newsletters';
import type { Newsletter } from '@/types/newsletter';

const props = defineProps<{
  newsletter: Newsletter | null;
}>();

const emit = defineEmits<{
  close: [];
}>();

const loading = ref(false);

const sendNewsletter = async () => {
  if (!props.newsletter) return;
  
  if (!confirm('Вы уверены, что хотите отправить эту рассылку?')) return;
  
  loading.value = true;
  
  try {
    await newsletterService.sendNewsletter(props.newsletter.id);
    emit('close');
  } catch (error) {
    console.error('Ошибка отправки рассылки:', error);
    alert('Ошибка отправки рассылки');
  } finally {
    loading.value = false;
  }
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
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>
