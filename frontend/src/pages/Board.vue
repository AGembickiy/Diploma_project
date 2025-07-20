<template>
  <MainLayout>
    <AnnouncementList :announcements="announcements" />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import AnnouncementList from '@/components/ui/AnnouncementList.vue'
import type { Announcement } from '@/types/announcement'

const announcements = ref<Announcement[]>([
  {
    id: '1',
    title: 'Ищем танка в рейд',
    content: 'Набираем группу для прохождения нового рейда. **Требуется опытный танк** с хорошим снаряжением. Рейд состоится в субботу в 20:00.\n\n*Требования:*\n- Уровень 60+\n- Опыт в рейдах\n- Голосовой чат\n\nНаграды делятся поровну между всеми участниками.',
    category: 'tank',
    author: 'Гилдмастер_Алекс',
    createdAt: new Date('2024-01-15T10:30:00'),
    isActive: true,
    images: [
      'https://via.placeholder.com/400x300/4a90e2/ffffff?text=Рейд+Танк',
      'https://via.placeholder.com/400x300/8c7ae6/ffffff?text=Снаряжение'
    ]
  },
  {
    id: '2',
    title: 'Продажа зелий восстановления',
    content: 'Изготавливаю качественные зелья восстановления здоровья и маны. **Цены ниже рыночных!**\n\n*Доступные зелья:*\n- Зелье здоровья (большое) - 50 золота\n- Зелье маны (большое) - 45 золота\n- Зелье выносливости - 30 золота\n\nСкидки при покупке от 10 штук. Доставка по городу.',
    category: 'alchemist',
    author: 'Алхимик_Елена',
    createdAt: new Date('2024-01-14T15:45:00'),
    updatedAt: new Date('2024-01-15T09:20:00'),
    isActive: true
  },
  {
    id: '3',
    title: 'Квест: Сбор редких трав',
    content: 'Нужны редкие травы для создания эликсира. **Награда: 200 золота + редкий рецепт**\n\n*Требуемые травы:*\n- Лунная трава (5 штук)\n- Звездный лотос (3 штуки)\n- Огненный мох (10 штук)\n\nСрок выполнения: 3 дня. Обращаться к квестгиверу в таверне.',
    category: 'questgiver',
    author: 'Квестгивер_Маркус',
    createdAt: new Date('2024-01-13T12:15:00'),
    isActive: true
  },
  {
    id: '4',
    title: 'Ремонт оружия и брони',
    content: 'Профессиональный ремонт оружия и брони. **Гарантия качества!**\n\n*Услуги:*\n- Заточка оружия\n- Починка брони\n- Улучшение снаряжения\n- Создание новых предметов\n\nРаботаю в кузнице на главной площади. Цены договорные.',
    category: 'blacksmith',
    author: 'Кузнец_Торин',
    createdAt: new Date('2024-01-12T08:30:00'),
    isActive: true,
    videos: [
      'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4'
    ]
  },
  {
    id: '5',
    title: 'Гильдия ищет новых членов',
    content: 'Гильдия "Хранители Света" приглашает активных игроков. **Открыт набор во все классы!**\n\n*Преимущества гильдии:*\n- Совместные рейды\n- Обучение новичков\n- Банк гильдии\n- Голосовой чат\n\nТребования: уровень 50+, активность в игре.',
    category: 'guildmaster',
    author: 'Гилдмастер_Светлана',
    createdAt: new Date('2024-01-11T16:20:00'),
    isActive: false
  }
])
</script> 