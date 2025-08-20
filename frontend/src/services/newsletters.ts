import axios from 'axios';
import type {
  Newsletter,
  NewsletterCreate,
  NewsletterTemplate,
  NewsletterRecipient,
  NewsletterStats,
  NewsletterPreview,
  NewsletterResponse
} from '@/types/newsletter';

const API_BASE_URL = 'http://localhost:8000/api';

// Настройка axios с токеном авторизации
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для добавления токена
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const newsletterService = {
  // Получить все рассылки
  async getNewsletters(): Promise<Newsletter[]> {
    const response = await api.get('/newsletters/');
    return response.data.results || response.data;
  },

  // Получить рассылку по ID
  async getNewsletter(id: number): Promise<Newsletter> {
    const response = await api.get(`/newsletters/${id}/`);
    return response.data;
  },

  // Создать новую рассылку
  async createNewsletter(data: NewsletterCreate): Promise<Newsletter> {
    const response = await api.post('/newsletters/', data);
    return response.data;
  },

  // Обновить рассылку
  async updateNewsletter(id: number, data: Partial<NewsletterCreate>): Promise<Newsletter> {
    const response = await api.patch(`/newsletters/${id}/`, data);
    return response.data;
  },

  // Удалить рассылку
  async deleteNewsletter(id: number): Promise<void> {
    await api.delete(`/newsletters/${id}/`);
  },

  // Отправить рассылку
  async sendNewsletter(id: number): Promise<NewsletterResponse> {
    const response = await api.post(`/newsletters/${id}/send/`);
    return response.data;
  },

  // Отменить рассылку
  async cancelNewsletter(id: number): Promise<NewsletterResponse> {
    const response = await api.post(`/newsletters/${id}/cancel/`);
    return response.data;
  },

  // Дублировать рассылку
  async duplicateNewsletter(id: number): Promise<Newsletter> {
    const response = await api.post(`/newsletters/${id}/duplicate/`);
    return response.data;
  },

  // Предварительный просмотр рассылки
  async previewNewsletter(id: number): Promise<NewsletterPreview> {
    const response = await api.get(`/newsletters/${id}/preview/`);
    return response.data;
  },

  // Получить получателей рассылки
  async getNewsletterRecipients(id: number): Promise<NewsletterRecipient[]> {
    const response = await api.get(`/newsletters/${id}/recipients/`);
    return response.data;
  },

  // Получить статистику рассылок
  async getNewsletterStats(): Promise<NewsletterStats> {
    const response = await api.get('/newsletters/stats/');
    return response.data;
  },

  // Обработать запланированные рассылки
  async processScheduledNewsletters(): Promise<NewsletterResponse> {
    const response = await api.post('/newsletters/process_scheduled/');
    return response.data;
  },

  // Очистить старые рассылки
  async cleanupOldNewsletters(days: number = 30): Promise<NewsletterResponse> {
    const response = await api.post('/newsletters/cleanup/', { days });
    return response.data;
  },

  // Получить все шаблоны
  async getTemplates(): Promise<NewsletterTemplate[]> {
    const response = await api.get('/templates/');
    return response.data.results || response.data;
  },

  // Получить шаблон по ID
  async getTemplate(id: number): Promise<NewsletterTemplate> {
    const response = await api.get(`/templates/${id}/`);
    return response.data;
  },

  // Создать новый шаблон
  async createTemplate(data: Omit<NewsletterTemplate, 'id' | 'created_at'>): Promise<NewsletterTemplate> {
    const response = await api.post('/templates/', data);
    return response.data;
  },

  // Обновить шаблон
  async updateTemplate(id: number, data: Partial<NewsletterTemplate>): Promise<NewsletterTemplate> {
    const response = await api.patch(`/templates/${id}/`, data);
    return response.data;
  },

  // Удалить шаблон
  async deleteTemplate(id: number): Promise<void> {
    await api.delete(`/templates/${id}/`);
  },

  // Использовать шаблон для создания рассылки
  async useTemplate(id: number): Promise<Newsletter> {
    const response = await api.post(`/templates/${id}/use_template/`);
    return response.data;
  },

  // Получить получателей (с фильтрацией)
  async getRecipients(newsletterId?: number): Promise<NewsletterRecipient[]> {
    const params = newsletterId ? { newsletter_id: newsletterId } : {};
    const response = await api.get('/recipients/', { params });
    return response.data;
  },
};

export default newsletterService;
