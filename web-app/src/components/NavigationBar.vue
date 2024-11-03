<template>
  <nav class="flex justify-between items-center py-4 border-b">
    <router-link to="/" class="text-2xl font-bold text-gray-800">DJ Khaled's Animal Shelter</router-link>

    <div class="flex space-x-4 items-center">
      <!-- role-based actions -->
      <div v-if="isLoggedIn" class="relative">
        <button @click="toggleActions" class="text-gray-800 font-semibold bg-gray-200 py-2 px-4 rounded-lg hover:bg-gray-300">
          Actions
        </button>
        <!-- dropdown for role-based actions -->
        <div v-if="showActions" class="absolute right-0 mt-2 bg-white shadow-lg rounded-lg py-2 w-48 z-10">
          <router-link v-for="action in roleActions" :key="action.name" :to="action.link" class="block px-4 py-2 hover:bg-gray-100">
            {{ action.name }}
          </router-link>
        </div>
      </div>

      <router-link v-if="!isLoggedIn" to="/login" class="bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-600">
        Login
      </router-link>
      <router-link v-else to ="/profile" class="bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">
        My Profile
      </router-link>
      <!-- <button v-if="isLoggedIn" @click="clickProfile" class="bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">
        My Profile
      </button> -->

      <button v-if="isLoggedIn" @click="handleLogout" class="bg-red-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-600">
        Logout
      </button>
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
          { name: 'Manage Animals', link: '/manage-animals' },
          { name: 'List users', link: '/listusers' },
          { name: 'Add animal', link: '/addanimal' },
        ];
      } else if (this.userRole === 'veterinarian') {
        return [
          { name: 'Medical Records', link: '/medical-records' }
        ];
      } else if (this.userRole === 'volunteer') {
        return [
          { name: 'Task List', link: '/tasks' },
        ];
      } else if (this.userRole === 'admin') {
        return [
          { name: 'List users', link: '/listusers' },
          { name: 'Add animal', link: '/addanimal' },
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
