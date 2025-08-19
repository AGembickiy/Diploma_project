import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

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
      title: 'Доска объявлений',
      requiresAuth: true
    }
  },
  {
    path: '/responses',
    name: 'Responses',
    component: () => import('@/pages/Responses.vue'),
    meta: {
      title: 'Отклики',
      requiresAuth: true
    }
  },
  {
    path: '/verify-email',
    name: 'VerifyEmail',
    component: () => import('@/pages/VerifyEmail.vue'),
    meta: {
      title: 'Подтверждение Email'
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

// Глобальный guard для установки заголовков страниц и проверки авторизации
router.beforeEach((to, _from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - Дипломный проект`
  }
  
  // Проверка авторизации для защищенных роутов
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    if (userStore.isGuest) {
      // Перенаправляем на главную страницу, если пользователь не авторизован
      next('/')
      return
    }
  }
  
  next()
})

export default router 