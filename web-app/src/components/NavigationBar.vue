<template>
  <nav class="flex justify-between items-center py-4 border-b">
    <div class="text-2xl font-bold text-gray-800">DJ Khaled's Animal Shelter</div>
    
    <div class="flex space-x-4 items-center">
      <!-- Role-based actions -->
      <div v-if="isLoggedIn" class="relative">
        <button @click="toggleActions" class="text-gray-800 font-semibold bg-gray-200 py-2 px-4 rounded-lg hover:bg-gray-300">
          Actions
        </button>
        <!-- Dropdown for role-based actions -->
        <div v-if="showActions" class="absolute right-0 mt-2 bg-white shadow-lg rounded-lg py-2 w-48 z-10">
          <router-link v-for="action in roleActions" :key="action.name" :to="action.link" class="block px-4 py-2 hover:bg-gray-100">
            {{ action.name }}
          </router-link>
        </div>
      </div>

      <!-- Profile or Login button -->
      <router-link v-if="!isLoggedIn" to="/login" class="bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-600">
        Login
      </router-link>
      <router-link v-else to="/profile" class="bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">
        My Profile
      </router-link>

      <!-- Logout button -->
      <button v-if="isLoggedIn" @click="handleLogout" class="bg-red-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-600">
        Logout
      </button>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      showActions: false,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole', 'tokenExp']),

    isLoggedIn() {
      return this.isAuthenticated;
    },

    roleActions() {
      if (this.userRole === 'caregiver') {
        return [
          { name: 'Caregiver Dashboard', link: '/caregiver-dashboard' },
          { name: 'Manage Animals', link: '/manage-animals' }
        ];
      } else if (this.userRole === 'veterinarian') {
        return [
          { name: 'Veterinarian Dashboard', link: '/veterinarian-dashboard' },
          { name: 'Medical Records', link: '/medical-records' }
        ];
      } else if (this.userRole === 'volunteer') {
        return [
          { name: 'Volunteer Dashboard', link: '/volunteer-dashboard' },
          { name: 'Task List', link: '/tasks' }
        ];
      }
      return []; // Empty for unauthenticated or unknown roles
    }
  },
  mounted() {
    this.checkExpiredToken();

    this.tokenInterval = setInterval(() => {
      this.checkExpiredToken();
    }, 120000);
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
    checkExpiredToken() {

      console.log("Checking token expiration...");
      console.log(Date.now());
      console.log(this.$store.state.expiration * 1000);

      if((Date.now() >= this.tokenExp * 1000) && this.isLoggedIn) {
        alert("Your session has expired. Please log in again.");
        this.handleLogout();
      }
    }
  },
  beforeUnmount() {
    clearInterval(this.tokenInterval);
  }
};
</script>