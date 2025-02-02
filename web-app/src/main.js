import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'
import store from './auth'


createApp(App).use(router).use(store).mount('#app')