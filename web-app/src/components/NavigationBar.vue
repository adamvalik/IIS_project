<template>
  <nav class="flex justify-between items-center py-4 border-b">

    <router-link to="/" class="text-2xl font-bold text-gray-800 flex gap-2">
      <img src="/assets/logo.png" alt="Logo" class="h-8 object-cover" />
      DJ Khaled's Animal Shelter
    </router-link>

    <div class="flex space-x-4 items-center">

      <router-link v-if="!isLoggedIn" to="/login" class="bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-150">
        Login
      </router-link>
      <router-link v-else to ="/profile" class="bg-green-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-600 transition duration-150">
        My Profile
      </router-link>

      <!-- role-based actions -->
      <div v-if="isLoggedIn" class="relative">
        <button @click="toggleActions" class="text-white font-semibold bg-blue-500 py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-150">
          Actions
        </button>
        <!-- dropdown for role-based actions -->
        <transition
          name="dropdown"
          enter-active-class="transition ease-out duration-300 transform"
          enter-from-class="opacity-0 scale-90"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200 transform"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-90"
        >

          <div v-if="showActions" class="absolute right-0 mt-4 bg-white p-2 shadow-lg rounded-lg py-2 w-64 z-10">
            <router-link
              v-for="action in roleActions"
              :key="action.name"
              :to="action.link"
              class="block pl-4 py-2 rounded-md hover:bg-gray-100 transition duration-150"
              >
              {{ action.name }}
            </router-link>
            <div class="flex justify-end items-center mr-3">
              <button v-if="isLoggedIn" @click="handleLogout" class="bg-red-500 text-white font-semibold py-1 px-4 rounded-lg hover:bg-red-600 transition duration-150">
                Logout
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </nav>
</template>

<script>
// import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      showActions: false,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole']),

    isLoggedIn() {
      return this.isAuthenticated;
    },

    roleActions() {
      if (this.userRole === 'caregiver') {
        return [
          { name: 'All animals 🐾', link: '/animals' },
          { name: 'Add animal 🐕', link: '/addanimal' },
          { name: 'Manage volunteers 👨🏻', link: '/listusers' },
          { name: 'Reservations 📝', link: '/reservations' },
          { name: 'Medical records 💉', link: '/medicalrecords' },
        ];
      } else if (this.userRole === 'veterinarian') {
        return [
          { name: 'Examination requests 🩺', link: '/requests' },
          { name: 'Medical records 💉', link: '/medicalrecords' },
        ];
      } else if (this.userRole === 'volunteer') {
        return [
          { name: 'My reservations 📝', link: '/reservations' },
          { name: 'All animals 🐾', link: '/animals' },
        ];
      } else if (this.userRole === 'admin') {
        return [
          { name: 'Manage users 👨🏻', link: '/listusers' },
          { name: 'Add animal 🐕', link: '/addanimal' },
          { name: 'All animals 🐾', link: '/animals' },
          { name: 'Reservations 📝', link: '/reservations' },
          { name: 'Examination requests 🩺', link: '/requests' },
          { name: 'Medical records 💉', link: '/medicalrecords' },
        ];
      }
      return [];
    }
  },
  methods: {
    toggleActions() {
      this.showActions = !this.showActions;
    },
    handleLogout() {
      // Dispatch the logout action from Vuex
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    async clickProfile() {
      this.$router.push('/profile');
    }
},
beforeUnmount() {
  clearInterval(this.tokenInterval);
}
};
</script>
