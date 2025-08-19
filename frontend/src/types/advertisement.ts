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

export interface User {
  id: number
  username: string
  email: string
  email_verified: boolean
  date_joined: string
}

export interface Advertisement {
  id: number
  title: string
  description: string
  category: AdvertisementCategory
  author: User
  image?: string
  video?: string
  audio?: string
  created_at: string
  updated_at: string
  responses?: Response[]
}

export interface AdvertisementCreate {
  title: string
  description: string
  category: AdvertisementCategory
  image?: File
  videoFile?: File
  audioFile?: File
}

export interface Response {
  id: number
  advertisement: Advertisement
  author: User
  text: string
  status: 'new' | 'accepted' | 'rejected'
  created_at: string
  updated_at: string
} 