import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Импорт normalize.css для кроссбраузерной совместимости
import 'normalize.css'

// Импорт глобальных стилей
import '@/assets/styles/fonts.css'
import '@/assets/styles/base.css'

const app = createApp(App)

// Подключение Pinia для управления состоянием
app.use(createPinia())

// Подключение роутера
app.use(router)

// Монтирование приложения
app.mount('#app') 