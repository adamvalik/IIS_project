import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import AnimalsView from '@/views/AnimalsView.vue'
import AnimalDetail from '@/components/AnimalDetail.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/signup', component: SignUpView },
  { path: '/animals', component: AnimalsView },
  { path: '/animal/:id', component: AnimalDetail }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
