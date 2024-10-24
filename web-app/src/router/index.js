import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import AnimalsView from '@/views/AnimalsView.vue'
import AnimalDetail from '@/components/AnimalDetail.vue'
import SchedulerView from '../views/SchedulerView.vue' // Import the Scheduler component
import HomePageView from '@/views/HomePageView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/signup', component: SignUpView },
  { path: '/animals', component: AnimalsView },
  { path: '/animal/:id', component: AnimalDetail },
  { path: '/scheduler', component: SchedulerView }, // Define the route for Scheduler
  { path:  '/homepage', component: HomePageView }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
