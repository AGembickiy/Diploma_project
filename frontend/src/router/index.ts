import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Main',
    component: () => import('@/pages/Main.vue'),
    meta: {
      title: 'Главная'
    }
  },
  {
    path: '/board',
    name: 'Board',
    component: () => import('@/pages/Board.vue'),
    meta: {
      title: 'Доска объявлений'
    }
  },
  {
    path: '/responses',
    name: 'Responses',
    component: () => import('@/pages/Responses.vue'),
    meta: {
      title: 'Отклики'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFound.vue'),
    meta: {
      title: 'Страница не найдена'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Глобальный guard для установки заголовков страниц
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - Дипломный проект`
  }
  next()
})

export default router 