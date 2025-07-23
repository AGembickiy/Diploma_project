export type AdvertisementCategory = 
  | 'Танки'
  | 'Хилы'
  | 'ДД'
  | 'Торговцы'
  | 'Гилдмастеры'
  | 'Квестгиверы'
  | 'Кузнецы'
  | 'Кожевники'
  | 'Зельевары'
  | 'Мастера заклинаний'

export interface Advertisement {
  id: number
  title: string
  description: string
  category: AdvertisementCategory
  image: string
  createdAt: Date
  media?: {
    images?: string[]
    video?: boolean
    audio?: boolean
  }
} 