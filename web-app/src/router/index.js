import { createRouter, createWebHistory } from 'vue-router'
import store from '../auth';
import axios from 'axios';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import SignUpView from '@/views/SignUpView.vue';
import AnimalsView from '@/views/AnimalsView.vue';
import AnimalDetail from '@/components/AnimalDetail.vue';
import SchedulerView from '@/views/SchedulerView.vue'; // Import the Scheduler component
import ProfileDetail from "@/components/ProfileDetail.vue";
import ListUsersView from '@/views/ListUsersView.vue'
import AddAnimalView from '@/views/AddAnimalView.vue';
import ReservationsView from '@/views/ReservationsView.vue';
import UserDetail from "@/views/UserDetail.vue";
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
  { path: '/requests', component: RequestsView }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

const protectedRoutes = ['/profile', '/scheduler', '/listusers', '/addanimal'];
const userInfoRoutes = /^\/user\/\d+$/;
const loginRoutes = ['/login', '/signup'];
const BASE_URL = 'http://localhost:8000';

router.beforeEach(async (to, from, next) => {
  console.log('token:', store.getters.tokenExp);
  console.log('role:', store.getters.userRole);
  console.log('id:', store.getters.user_id);
  console.log('auth:', store.getters.isAuthenticated);

  const token = store.state.accessToken; // Get the token from Vuex store

  if (protectedRoutes.includes(to.path) || userInfoRoutes.test(to.path)) {

    // const fakeToken = 'fake';
    // If the token is not available, redirect to the login page
    if (!token) {
      alert('You must be logged in to view this page.');
      return next('/login'); // Redirect to the login page
    }

    // If the token is present, verify it with the backend
    try {
      console.log('Fetching protected route:',to.path);
      await axios.get(`${BASE_URL}${to.path}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      next(); // Proceed to the requested route if the token is valid
    } catch (error) {
      if (error.response) {
        console.error('Error fetching protected route:', error.response.data.detail); // Print error detail
        console.error('Status code:', error.response.status); // Print status code
      } else {
        console.error('Error fetching protected route:', error.message);
      }
      alert(error.response.data.detail);
      next('/'); // Redirect to the login page on failure
    }
  } else if(loginRoutes.includes(to.path) && store.state.accessToken) {
    next('/');
  } else {
    next(); // Proceed to non-protected routes
  }
});


// // Set up a global before guard to protect routes
// router.beforeEach((to, from, next) => {
//   const isAuthenticated = !!localStorage.getItem('access_token'); // Check if token exists in localStorage

//   // Define routes that require authentication
//   const publicPages = ['/login', '/', '/signup']; // Add public routes here
//   const authRequired = !publicPages.includes(to.path);

//   // If the route requires authentication and the user is not authenticated
//   if (authRequired && !isAuthenticated) {
//     next('/login'); // Redirect to login page
//   } else if (isAuthenticated && (to.path === '/login' || to.path === '/signup')) {
//     next('/'); // Redirect logged-in users from login or signup to homepage
//   } else {
//     next(); // Proceed to the requested route
//   }
// });

// router/index.js
// import { createRouter, createWebHistory } from 'vue-router';
// import store from '../store'; // Import your Vuex store
// import Home from '../views/Home.vue';
// import CaregiverDashboard from '../views/CaregiverDashboard.vue'; // Example view

// const routes = [
//   { path: '/', component: Home },
//   {
//     path: '/caregiver-dashboard',
//     component: CaregiverDashboard,
//     meta: { requiresAuth: true, role: 'caregiver' } // Define meta properties
//   },
//   // Add other routes here
// ];

// const router = createRouter({
//   history: createWebHistory(process.env.BASE_URL),
//   routes
// });

// // Navigation guard
// router.beforeEach((to, from, next) => {
//   const isAuthenticated = store.getters.isAuthenticated;
//   const userRole = store.getters.userRole;

//   // Check if the route requires authentication
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     if (!isAuthenticated) {
//       // Redirect to login if not authenticated
//       next({ path: '/login' });
//     } else if (to.meta.role && to.meta.role !== userRole) {
//       // Redirect to home or another page if role does not match
//       next({ path: '/' }); // Change to your desired redirect
//     } else {
//       // Proceed to the route if authenticated and has the proper role
//       next();
//     }
//   } else {
//     // Proceed to the route if it does not require authentication
//     next();
//   }
// });

// export default router;


export default router
