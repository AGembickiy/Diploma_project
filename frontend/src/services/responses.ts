import axios from 'axios'
import type { Response, Advertisement } from '@/types/advertisement'

const API_BASE_URL = 'http://localhost:8000/api'

// Интерфейс для фильтров
interface ResponseFilters {
  advertisement_id?: number | 'all'
  status?: 'new' | 'accepted' | 'rejected' | 'all'
}

export class ResponsesService {
  private static getAuthHeaders() {
    const token = localStorage.getItem('auth_token')
    return {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  }

  /**
   * Получить все отклики на объявления текущего пользователя
   */
  static async getMyAdvertisementResponses(filters?: ResponseFilters): Promise<Response[]> {
    try {
      const params = new URLSearchParams()
      if (filters?.advertisement_id && filters.advertisement_id !== 'all') {
        params.append('advertisement_id', filters.advertisement_id.toString())
      }
      if (filters?.status && filters.status !== 'all') {
        params.append('status', filters.status)
      }

      const response = await axios.get(
        `${API_BASE_URL}/responses/advertisement_responses/`,
        {
          headers: this.getAuthHeaders(),
          params
        }
      )
      return response.data
    } catch (error) {
      console.error('Ошибка при получении откликов:', error)
      throw error
    }
  }

  /**
   * Получить все объявления текущего пользователя
   */
  static async getMyAdvertisements(): Promise<Advertisement[]> {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/advertisements/my_advertisements/`,
        {
          headers: this.getAuthHeaders()
        }
      )
      return response.data
    } catch (error) {
      console.error('Ошибка при получении объявлений:', error)
      throw error
    }
  }

  /**
   * Изменить статус отклика
   */
  static async changeResponseStatus(responseId: number, status: 'accepted' | 'rejected'): Promise<Response> {
    try {
      const response = await axios.patch(
        `${API_BASE_URL}/responses/${responseId}/change_status/`,
        { status },
        {
          headers: this.getAuthHeaders()
        }
      )
      return response.data
    } catch (error: any) {
      console.error(`❌ Ошибка при изменении статуса отклика ${responseId}:`, error)
      if (error.response?.status === 404) {
        throw new Error(`Отклик с ID ${responseId} не найден`)
      } else if (error.response?.status === 403) {
        throw new Error('У вас нет прав для изменения этого отклика')
      } else {
        throw new Error(`Ошибка сервера: ${error.response?.data?.detail || error.message}`)
      }
    }
  }

  /**
   * Удалить отклик
   */
  static async deleteResponse(responseId: number): Promise<void> {
    try {
      await axios.delete(
        `${API_BASE_URL}/responses/${responseId}/`,
        {
          headers: this.getAuthHeaders()
        }
      )
    } catch (error: any) {
      console.error(`❌ Ошибка при удалении отклика ${responseId}:`, error)
      if (error.response?.status === 404) {
        throw new Error(`Отклик с ID ${responseId} не найден`)
      } else if (error.response?.status === 403) {
        throw new Error('У вас нет прав для удаления этого отклика')
      } else {
        throw new Error(`Ошибка сервера: ${error.response?.data?.detail || error.message}`)
      }
    }
  }
}
