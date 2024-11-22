import { createRouter, createWebHistory } from 'vue-router'
import store from '../auth';
import apiClient from '@/api';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import SignUpView from '@/views/SignUpView.vue';
import AnimalsView from '@/views/AnimalsView.vue';
import AnimalDetail from '@/views/AnimalDetail.vue';
import SchedulerView from '@/views/SchedulerView.vue'; // Import the Scheduler component
import ProfileDetail from "@/views/ProfileDetail.vue";
import ListUsersView from '@/views/ListUsersView.vue'
import AddAnimalView from '@/views/AddAnimalView.vue';
import ReservationsView from '@/views/ReservationsView.vue';
import UserDetail from "@/views/UserDetail.vue";
import MedicalRecordsList from "@/views/MedicalRecordsList.vue";
import RequestsView from '@/views/RequestsView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/signup', component: SignUpView },
  { path: '/animals', component: AnimalsView },
  { path: '/animal/:id', component: AnimalDetail },
  { path: '/scheduler/:id', component: SchedulerView },
  { path: '/profile', component: ProfileDetail },
  { path: '/listusers', component: ListUsersView},
  { path: '/addanimal', component: AddAnimalView },
  { path: '/reservations', component: ReservationsView },
  { path: '/user/:id', component: UserDetail },
  { path: '/requests', component: RequestsView },
  { path: '/medicalrecords/:id', component: MedicalRecordsList },
  { path: '/medicalrecords', component: MedicalRecordsList }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Specify routes that require authentication
const protectedRoutes = ['/profile', '/listusers', '/addanimal', '/reservations', '/requests'];
const userInfoRoutes = /^\/user\/\d+$/;
const schedulerRoutes = /^\/scheduler\/\d+$/;
const medicalRecordsRoutes = /^\/medicalrecords\/\d+$/;
const loginRoutes = ['/login', '/signup'];

router.beforeEach(async (to, from, next) => {

  // Obtain token from Vuex store
  const token = store.state.accessToken;

  // If the requested route is protected, verify the token
  if (protectedRoutes.includes(to.path) ||
      userInfoRoutes.test(to.path) ||
      schedulerRoutes.test(to.path) ||
      medicalRecordsRoutes.test(to.path)) {

    // If the token does not exist, redirect to the login page
    if (!token) {
      alert('You must be logged in to view this page.');
      return next('/login');
    }

    // Try to proceed to the requested route by sending a request to the backend with authenticaton headers
    try {
      await apiClient.get(to.path);
      //Proceed to the requested route if the token is valid
      next();
    } catch (error) {
      if (error.response) {
        console.error('Error fetching protected route:', error.response.data.detail);
        console.error('Status code:', error.response.status);
      } else {
        console.error('Error fetching protected route:', error.message);
      }

      // If the token is invalid, redirect to the home page
      alert(error.response.data.detail);
      next('/');
    }

    // If the user is already logged in, redirect to the home page
  } else if(loginRoutes.includes(to.path) && token) {

    
    next('/');
  } else {
    // Redirect to the requested route if it is not protected
    next();
  }
});


export default router
