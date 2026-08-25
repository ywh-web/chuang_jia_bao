import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

window.__CHAoyun_API_BASE__ = import.meta.env.VITE_API_BASE_URL || ''

import routes from './router'

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' }),
})

createApp(App).use(router).mount('#app')

