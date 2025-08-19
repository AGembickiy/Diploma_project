export interface Announcement {
  id: string;
  title: string;
  content: string;
  category: AnnouncementCategory;
  author: string;
  createdAt: Date;
  updatedAt?: Date;
  images?: string[];
  videos?: string[];
  isActive: boolean;
}

export type AnnouncementCategory = 
  | 'tank'           // Танки
  | 'healer'         // Хилы
  | 'dd'             // ДД
  | 'merchant'       // Торговцы
  | 'guildmaster'    // Гилдмастеры
  | 'questgiver'     // Квестгиверы
  | 'blacksmith'     // Кузнецы
  | 'leatherworker'  // Кожевники
  | 'alchemist'      // Зельевары
  | 'spellmaster';   // Мастера заклинаний

export interface AnnouncementCategoryInfo {
  value: AnnouncementCategory;
  label: string;
  icon: string;
  color: string;
}

export const ANNOUNCEMENT_CATEGORIES: AnnouncementCategoryInfo[] = [
  {
    value: 'tank',
    label: 'Танки',
    icon: '/src/assets/images/icons/tank_icon.png',
    color: '#4a90e2'
  },
  {
    value: 'healer',
    label: 'Хилы',
    icon: '/src/assets/images/icons/healer_icon.png',
    color: '#50c878'
  },
  {
    value: 'dd',
    label: 'ДД',
    icon: '/src/assets/images/icons/dd_icon.png',
    color: '#ff6b6b'
  },
  {
    value: 'merchant',
    label: 'Торговцы',
    icon: '/src/assets/images/icons/merchant_icon.png',
    color: '#ffd93d'
  },
  {
    value: 'guildmaster',
    label: 'Гилдмастеры',
    icon: '/src/assets/images/icons/guildmaster_icon.png',
    color: '#9b59b6'
  },
  {
    value: 'questgiver',
    label: 'Квестгиверы',
    icon: '/src/assets/images/icons/questgiver_icon.png',
    color: '#e67e22'
  },
  {
    value: 'blacksmith',
    label: 'Кузнецы',
    icon: '/src/assets/images/icons/blacksmith_icon.png',
    color: '#8b4513'
  },
  {
    value: 'leatherworker',
    label: 'Кожевники',
    icon: '/src/assets/images/icons/leatherworker_icon.png',
    color: '#d2691e'
  },
  {
    value: 'alchemist',
    label: 'Зельевары',
    icon: '/src/assets/images/icons/alchemist_icon.png',
    color: '#20b2aa'
  },
  {
    value: 'spellmaster',
    label: 'Мастера заклинаний',
    icon: '/src/assets/images/icons/spellmaster_icon.png',
    color: '#9370db'
  }
]; 