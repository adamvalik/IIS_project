import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SchedulerView from '../views/SchedulerView.vue' // Import the Scheduler component

const routes = [
  { path: '/', component: HomeView },
  { path: '/scheduler', component: SchedulerView } // Define the route for Scheduler
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
