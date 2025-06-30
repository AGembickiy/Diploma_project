# 🏗️ Универсальная архитектурная шпаргалка Vue 3

## 📋 Общая информация

**Технологический стек:**
- **Frontend:** Vue 3.2.13 + Composition API
- **Роутинг:** Vue Router 4.0.3
- **Состояние:** Pinia (приоритет) / Vuex 4.0.0 (legacy) + Composition API hooks
- **HTTP клиент:** Axios 1.10.0
- **Стили:** CSS Variables + normalize.css
- **Сборка:** Vue CLI 5.0.0
- **Язык:** TypeScript (приоритет) / JavaScript (legacy)

**Архитектура:** Модульная архитектура с разделением на слои

---

## 🎯 Основные принципы архитектуры

### 1. **TypeScript First**
- ✅ Используем TypeScript для всех новых файлов
- ✅ JavaScript только для legacy компонентов
- ✅ Строгая типизация для API и состояний
- ✅ Интерфейсы для всех структур данных

### 2. **Composition API First**
- ✅ Используем Composition API как основной подход
- ✅ Options API только для legacy компонентов
- ✅ Hooks для переиспользуемой логики

### 3. **Модульность**
- ✅ Каждый модуль в отдельной папке
- ✅ Четкое разделение ответственности
- ✅ Минимальные зависимости между модулями

### 4. **Переиспользуемость**
- ✅ UI компоненты как строительные блоки
- ✅ Hooks для бизнес-логики
- ✅ Директивы для DOM манипуляций

---

## 📁 Универсальная структура папок

```
src/
├── assets/           # Статические ресурсы
│   ├── styles/       # Глобальные стили
│   │   ├── variables.css # CSS переменные и темы
│   │   ├── base.css      # Базовые стили
│   │   └── utilities.css # Утилитарные классы
│   ├── images/       # Изображения (PNG, JPG, SVG, WebP)
│   │   ├── logos/    # Логотипы
│   │   ├── icons/    # Иконки
│   │   ├── backgrounds/ # Фоновые изображения
│   │   └── content/  # Контентные изображения
│   ├── videos/       # Видео файлы (MP4, WebM)
│   ├── audio/        # Аудио файлы (MP3, WAV, OGG)
│   └── fonts/        # Шрифты (WOFF, WOFF2, TTF)
├── components/       # Vue компоненты
│   ├── UI/          # Переиспользуемые UI компоненты
│   ├── Layout/      # Компоненты макета
│   └── Feature/     # Специфичные компоненты
├── composables/     # Composition API hooks
├── directives/      # Vue директивы
├── pages/           # Страницы приложения
├── views/           # Представления (альтернатива pages)
├── plugins/         # Плагины
├── router/          # Конфигурация роутинга
├── services/        # API сервисы
├── types/           # TypeScript типы и интерфейсы
├── utils/           # Утилиты и хелперы
├── constants/       # Константы
└── config/          # Конфигурация приложения
└── stores/          # Pinia stores (приоритет) / Vuex модули (legacy)
```

---

## 🎨 UI/UX Правила

### **CSS Variables System**
```css
/* Всегда используйте CSS переменные вместо хардкода */
.my-component {
  background-color: var(--primary-color);
  padding: var(--spacing-medium);
  font-size: var(--font-size-medium);
  border-radius: var(--border-radius);
}

/* Для состояний используйте модификаторы */
.my-component--disabled {
  opacity: var(--opacity-disabled);
  cursor: var(--cursor-disabled);
}

/* Для тем используйте переопределение переменных */
body.dark-theme {
  --primary-color: var(--dark-primary);
  --text-color: var(--dark-text);
}
```

### **Правила применения CSS переменных**
- ✅ **Всегда** используйте `var(--variable-name)` вместо хардкода
- ✅ Группируйте переменные по категориям (цвета, размеры, шрифты)
- ✅ Используйте семантичные имена переменных
- ✅ Поддерживайте темную тему через переопределение переменных
- ✅ Применяйте адаптивность через медиа-запросы с переменными

### **Компонентные правила**
- ✅ Используем CSS переменные для всех стилей
- ✅ Scoped стили для компонентов
- ✅ Адаптивный дизайн с медиа-запросами
- ✅ Консистентные отступы и размеры

---

## 🖼️ Медиа-файлы и ресурсы

### **Структура медиа-файлов**
```
assets/
├── images/
│   ├── logos/        # Логотипы компании/приложения
│   ├── icons/        # Иконки интерфейса
│   ├── backgrounds/  # Фоновые изображения
│   └── content/      # Контентные изображения
├── videos/           # Видео контент
├── audio/            # Аудио файлы
└── fonts/            # Кастомные шрифты
```

### **Правила именования медиа-файлов**
```typescript
// ✅ Используйте kebab-case для имен файлов
logo-primary.svg
user-avatar-default.png
background-hero.webp
icon-search.svg

// ✅ Группируйте по размерам/вариантам
logo-primary-32x32.svg
logo-primary-64x64.svg
logo-primary-dark.svg
logo-primary-light.svg
```

### **Оптимизация изображений**
```vue
<template>
  <!-- ✅ Используйте современные форматы -->
  <img src="@/assets/images/logo.webp" alt="Logo" />
  
  <!-- ✅ Добавляйте fallback для старых браузеров -->
  <picture>
    <source srcset="@/assets/images/hero.webp" type="image/webp" />
    <img src="@/assets/images/hero.jpg" alt="Hero image" />
  </picture>
  
  <!-- ✅ Используйте lazy loading для больших изображений -->
  <img 
    src="@/assets/images/content/large-image.jpg" 
    alt="Large content"
    loading="lazy"
  />
</template>
```

### **Правила работы с медиа**
- ✅ **Изображения:** Используйте WebP как основной формат, JPG/PNG как fallback
- ✅ **Иконки:** Предпочитайте SVG для масштабируемости
- ✅ **Логотипы:** Храните в векторном формате (SVG)
- ✅ **Видео:** Используйте MP4 (H.264) и WebM для лучшей совместимости
- ✅ **Аудио:** MP3 для музыки, WAV для звуковых эффектов
- ✅ **Шрифты:** WOFF2 для современной поддержки, WOFF как fallback

### **Импорт медиа-файлов**
```typescript
// ✅ Используйте алиасы для импорта
import logo from '@/assets/images/logos/logo-primary.svg'
import heroBg from '@/assets/images/backgrounds/hero.webp'
import customFont from '@/assets/fonts/custom-font.woff2'

// ✅ Для динамических импортов
const getImageUrl = (name: string): string => {
  return new URL(`../assets/images/${name}`, import.meta.url).href
}
```

### **Responsive изображения**
```vue
<template>
  <!-- ✅ Адаптивные изображения -->
  <img 
    :src="getResponsiveImage('hero', 'mobile')"
    :srcset="getResponsiveSrcset('hero')"
    sizes="(max-width: 768px) 100vw, 50vw"
    alt="Responsive hero"
  />
</template>

<script setup lang="ts">
const getResponsiveImage = (name: string, size: 'mobile' | 'desktop'): string => {
  return `/assets/images/${name}-${size}.webp`
}

const getResponsiveSrcset = (name: string): string => {
  return `/assets/images/${name}-mobile.webp 768w, /assets/images/${name}-desktop.webp 1200w`
}
</script>
```

### **Оптимизация производительности**
- ✅ Сжимайте изображения перед добавлением в проект
- ✅ Используйте правильные размеры (не растягивайте маленькие изображения)
- ✅ Применяйте lazy loading для изображений ниже fold
- ✅ Кэшируйте статические ресурсы
- ✅ Используйте CDN для больших медиа-файлов в продакшене

---

## 🔧 Composition API Hooks (Composables)

### **Структура типизированного composable**
```typescript
// composables/useHookName.ts
import { ref, computed, Ref, ComputedRef } from 'vue'

interface HookState {
  // типы состояния
}

interface HookReturn {
  // типы возвращаемых значений
}

export function useHookName(): HookReturn {
  // 1. Состояние (ref/reactive) с типизацией
  const state = ref<HookState>(initialValue)
  
  // 2. Computed свойства с типизацией
  const computedValue = computed<ComputedType>(() => /* логика */)
  
  // 3. Методы с типизацией
  const method = (param: ParamType): ReturnType => { /* логика */ }
  
  // 4. Возвращаем типизированный API
  return {
    state,
    computedValue,
    method
  }
}
```

### **Основные composables**
- `useApi()` - работа с API
- `useLocalStorage()` - работа с localStorage
- `useDebounce()` - debounce функциональность
- `useThrottle()` - throttle функциональность
- `useIntersectionObserver()` - наблюдение за элементами
- `useMediaQuery()` - медиа-запросы
- `useEventListener()` - обработка событий

---

## 🎭 Компонентные правила

### **Типизированные UI Компоненты**
```vue
<template>
  <button :class="buttonClasses" @click="handleClick">
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  disabled: false,
  title: ''
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => [
  'my-button',
  `my-button--${props.variant}`,
  `my-button--${props.size}`,
  { 'my-button--disabled': props.disabled }
])

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>
```

### **Правила именования**
- ✅ UI компоненты: `My` + `Name` (MyButton, MyInput)
- ✅ Страницы: PascalCase (Home.vue, UserProfile.vue)
- ✅ Composables: `use` + `Name` (useApi, useLocalStorage)
- ✅ Директивы: camelCase (clickOutside, focus)
- ✅ Типы: PascalCase (User, Post, ApiResponse)
- ✅ Интерфейсы: PascalCase с префиксом I (IUser, IPost)

---

## 🌐 API и сервисы

### **Типизированная структура сервиса**
```typescript
// services/api.ts
import { ApiResponse, User, CreateUserData } from '@/types'

export const userService = {
  async getAll(): Promise<User[]> {
    try {
      const response = await apiClient.get<ApiResponse<User[]>>('/users')
      return response.data.data
    } catch (error) {
      console.error('Error:', error)
      return [] // Fallback
    }
  },

  async create(userData: CreateUserData): Promise<User> {
    const response = await apiClient.post<ApiResponse<User>>('/users', userData)
    return response.data.data
  }
}
```

### **Правила API**
- ✅ Используем централизованный HTTP клиент
- ✅ Обработка ошибок с fallback данными
- ✅ Логирование ошибок в консоль
- ✅ Возврат пустых массивов вместо ошибок
- ✅ Типизация всех API методов
- ✅ Интерфейсы для request/response данных

---

## 🛣️ Роутинг

### **Типизированная структура маршрута**
```typescript
// router/index.ts
import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: {
      title: 'Главная',
      requiresAuth: false
    }
  }
]
```

### **Правила роутинга**
- ✅ Lazy loading для всех компонентов
- ✅ Мета-данные для заголовков страниц
- ✅ Семантичные имена маршрутов
- ✅ Группировка связанных маршрутов
- ✅ Типизация meta данных

---

## 🎯 Директивы

### **Типизированная структура директивы**
```typescript
// directives/clickOutside.ts
import { DirectiveBinding } from 'vue'

interface ClickOutsideBinding {
  handler: (event: Event) => void
  exclude?: HTMLElement[]
}

export default {
  name: 'clickOutside',
  mounted(el: HTMLElement, binding: DirectiveBinding<ClickOutsideBinding>) {
    // Логика при монтировании
  },
  unmounted(el: HTMLElement) {
    // Очистка при размонтировании
  }
}
```

### **Популярные директивы**
- `v-focus` - автофокус на элемент
- `v-click-outside` - обработка клика вне элемента
- `v-resize` - отслеживание изменения размера
- `v-scroll` - обработка прокрутки
- `v-tooltip` - всплывающие подсказки
- `v-permission` - проверка прав доступа
- `v-lazy` - ленивая загрузка изображений

---

## 🔄 Состояние приложения

### **Pinia (основной подход)**
```typescript
// В компоненте
const userStore = useUserStore()
const postsStore = usePostsStore()

// Деструктуризация с сохранением реактивности
const { user, isAuthenticated } = storeToRefs(userStore)
const { posts, isLoading } = storeToRefs(postsStore)
const { login, logout } = userStore
```

### **Composition API (для локального состояния)**
```typescript
// В компоненте
const { posts, isLoading, loadPosts } = usePosts()
const { searchQuery, filteredData } = useSearch(posts)
const { currentPage, paginatedData } = usePagination(filteredData)
```

### **Vuex (legacy)**
```typescript
// Модульная структура с типизацией
interface State {
  posts: Post[]
  isLoading: boolean
  error: string | null
}

export default {
  namespaced: true,
  state: (): State => ({ 
    posts: [],
    isLoading: false,
    error: null
  }),
  getters: { /* вычисляемые свойства */ },
  mutations: { /* синхронные изменения */ },
  actions: { /* асинхронные операции */ }
}
```

---

## 🎨 Стилизация

### **CSS Variables**
```css
/* Основные переменные */
:root {
  --primary-color: #42b883;
  --border-radius: 4px;
  --font-family: Arial, sans-serif;
}

/* Темная тема */
body.dark-theme {
  --text-color: #ffffff;
  --background-color: #1a1a1a;
}
```

### **Адаптивность**
```css
@media (max-width: 768px) {
  :root {
    --container-padding: 15px;
    --font-size-xl: 20px;
  }
}
```

---

## 🚀 Производительность

### **Оптимизации**
- ✅ Lazy loading компонентов
- ✅ Debounce для поиска
- ✅ Виртуализация для больших списков
- ✅ Кэширование API запросов
- ✅ Tree shaking для неиспользуемого кода
- ✅ Code splitting по маршрутам

### **Мониторинг**
- ✅ Логирование ошибок
- ✅ Отслеживание производительности
- ✅ Fallback данные при сбоях API
- ✅ Метрики Core Web Vitals

---

## 🔒 Безопасность

### **Правила**
- ✅ Валидация входных данных
- ✅ Санитизация пользовательского контента
- ✅ Проверка прав доступа через директивы
- ✅ Безопасная обработка ошибок
- ✅ CSP (Content Security Policy)
- ✅ XSS защита

---

## 📝 Код стайл

### **TypeScript/Vue**
- ✅ TypeScript для всех новых файлов
- ✅ Composition API для новых компонентов
- ✅ Строгая типизация
- ✅ Интерфейсы для всех структур данных
- ✅ Деструктуризация объектов
- ✅ Async/await для асинхронных операций

### **CSS**
- ✅ CSS Variables для темизации
- ✅ BEM методология для классов
- ✅ Scoped стили
- ✅ Адаптивный дизайн

---

## 🧪 Тестирование

### **Структура тестов**
```
tests/
├── unit/           # Unit тесты
├── integration/    # Интеграционные тесты
├── e2e/           # End-to-end тесты
└── __mocks__/     # Моки для тестов
```

### **Покрытие**
- ✅ Компоненты: 80%+
- ✅ Composables: 90%+
- ✅ Сервисы: 85%+

---

## 📦 Сборка и деплой

### **Скрипты**
```json
{
  "dev": "vite",
  "build": "vue-tsc && vite build",
  "preview": "vite preview",
  "type-check": "vue-tsc --noEmit",
  "test": "vitest",
  "lint": "eslint . --ext .vue,.js,.ts"
}
```

### **Конфигурация**
- ✅ Vite/Webpack с алиасами
- ✅ TypeScript компилятор
- ✅ ESLint + Prettier
- ✅ Оптимизация для продакшена

---

## 🔄 Миграции и обновления

### **План миграции**
1. ✅ Vue 2 → Vue 3 (завершено)
2. ✅ Options API → Composition API (в процессе)
3. ✅ JavaScript → TypeScript (в процессе)
4. ✅ Vuex → Pinia (приоритет для новых проектов)

### **Backward compatibility**
- ✅ Поддержка legacy компонентов
- ✅ Постепенная миграция
- ✅ Документирование изменений

---

## 📚 Документация

### **Обязательная документация**
- ✅ README.md для каждого модуля
- ✅ JSDoc для функций и методов
- ✅ Комментарии для сложной логики
- ✅ Примеры использования
- ✅ TypeScript интерфейсы

---

## 🎯 Чек-лист для новых компонентов

- [ ] Использует TypeScript
- [ ] Использует Composition API
- [ ] Использует Pinia для глобального состояния
- [ ] Имеет типизацию props
- [ ] Имеет валидацию props
- [ ] Использует CSS переменные
- [ ] Поддерживает адаптивность
- [ ] Имеет обработку ошибок
- [ ] Документирован
- [ ] Протестирован
- [ ] Следует naming conventions
- [ ] Оптимизированы медиа-файлы (если используются)
- [ ] Использует правильные форматы изображений
- [ ] Имеет alt-атрибуты для изображений

---

## 🚨 Анти-паттерны

### **Не делайте:**
- ❌ Не создавайте новые .js файлы
- ❌ Не используйте Options API для новых компонентов
- ❌ Не используйте Vuex для новых проектов (выбирайте Pinia)
- ❌ Не хардкодите стили
- ❌ Не игнорируйте обработку ошибок
- ❌ Не создавайте монолитные компоненты
- ❌ Не дублируйте логику между компонентами
- ❌ Не используйте `any` тип в TypeScript

### **Делайте:**
- ✅ Используйте TypeScript для всех новых файлов
- ✅ Используйте Pinia для управления состоянием
- ✅ Создавайте интерфейсы для всех структур данных
- ✅ Используйте composables для переиспользуемой логики
- ✅ Создавайте маленькие, специализированные компоненты
- ✅ Используйте CSS переменные
- ✅ Обрабатывайте все возможные ошибки
- ✅ Документируйте сложную логику
- ✅ Используйте строгую типизацию

### **Структура типов**
```typescript
// types/index.ts
export interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'user' | 'moderator'
}

export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface PaginationParams {
  page: number
  limit: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

// Типы для событий
export type ButtonVariant = 'primary' | 'secondary' | 'danger'
export type NotificationType = 'success' | 'error' | 'warning' | 'info'
```

---

## 🗃️ Pinia Store Management

### **Приоритет Pinia**
```typescript
// ✅ Используйте Pinia для управления состоянием
// ❌ Vuex только для legacy проектов

// Пример типизированного store
interface UserState {
  user: User | null
  isAuthenticated: boolean
  error: string | null
  loading: boolean
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    isAuthenticated: false,
    error: null,
    loading: false
  }),

  getters: {
    userName: (state): string => state.user?.name ?? 'Guest',
    isAdmin: (state): boolean => state.user?.role === 'admin',
    hasError: (state): boolean => !!state.error
  },

  actions: {
    async login(credentials: LoginCredentials) {
      this.loading = true
      this.error = null
      
      try {
        const user = await authService.login(credentials)
        this.user = user
        this.isAuthenticated = true
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.isAuthenticated = false
      this.error = null
    },

    clearError() {
      this.error = null
    }
  }
})
```

### **Правила создания stores**
- ✅ **Всегда** используйте `defineStore` для создания stores
- ✅ Создавайте интерфейсы для state
- ✅ Используйте семантичные имена (useUserStore, usePostsStore)
- ✅ Группируйте связанную логику в один store
- ✅ Используйте getters для вычисляемых значений
- ✅ Используйте actions для асинхронных операций

### **Структура stores**
```typescript
// stores/index.ts - главный файл для экспорта всех stores
export { useUserStore } from './user'
export { usePostsStore } from './posts'
export { useSettingsStore } from './settings'

// stores/user.ts - store для пользователей
export const useUserStore = defineStore('user', {
  state: () => ({ /* состояние */ }),
  getters: { /* вычисляемые свойства */ },
  actions: { /* методы */ }
})

// stores/posts.ts - store для постов
export const usePostsStore = defineStore('posts', {
  state: () => ({ /* состояние */ }),
  getters: { /* вычисляемые свойства */ },
  actions: { /* методы */ }
})
```

### **Использование в компонентах**
```vue
<template>
  <div>
    <p>Привет, {{ userStore.userName }}!</p>
    <button @click="userStore.logout">Выйти</button>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores'

const userStore = useUserStore()

// Деструктуризация с сохранением реактивности
const { user, isAuthenticated } = storeToRefs(userStore)
const { login, logout } = userStore
</script>
```

### **Composition API с Pinia**
```typescript
// composables/useAuth.ts
import { useUserStore } from '@/stores'

export function useAuth() {
  const userStore = useUserStore()

  const login = async (credentials: LoginCredentials) => {
    await userStore.login(credentials)
  }

  const logout = () => {
    userStore.logout()
  }

  return {
    user: computed(() => userStore.user),
    isAuthenticated: computed(() => userStore.isAuthenticated),
    login,
    logout
  }
}
```

### **Преимущества Pinia над Vuex**
- ✅ **Меньше boilerplate** - нет mutations, только actions
- ✅ **Лучшая TypeScript поддержка** - автоматический вывод типов
- ✅ **Меньший размер** - на 30-40% меньше кода
- ✅ **Лучшая производительность** - более эффективная реактивность
- ✅ **DevTools интеграция** - лучшая отладка
- ✅ **Composition API** - естественная интеграция

### **Миграция с Vuex на Pinia**
```typescript
// Старый Vuex код
const store = createStore({
  modules: {
    user: {
      namespaced: true,
      state: { user: null, isAuthenticated: false },
      getters: { userName: (state) => state.user?.name },
      mutations: { setUser: (state, user) => state.user = user },
      actions: { login: ({ commit }, credentials) => { /* логика */ } }
    }
  }
})

// Новый Pinia код
export const useUserStore = defineStore('user', {
  state: () => ({ user: null, isAuthenticated: false }),
  getters: { userName: (state) => state.user?.name },
  actions: { 
    setUser(user) { this.user = user },
    async login(credentials) { /* логика */ }
  }
})
```

---
