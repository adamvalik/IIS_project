<!-- Navbar.vue -->
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
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false, // Dynamic check for user login status
      showActions: false, // To control the display of the actions dropdown
      roleActions: [],
    };
  },
  mounted() {
    // Check if user is logged in
    this.isLoggedIn = this.checkUserLoginStatus();

    // Fetch actions based on user role
    if (this.isLoggedIn) {
      this.roleActions = this.getRoleBasedActions();
    }
  },
  methods: {
    toggleActions() {
      this.showActions = !this.showActions;
    },
    checkUserLoginStatus() {
      return localStorage.getItem("userToken") !== null;
    },
    getRoleBasedActions() {
      const userRole = this.getUserRole();
      if (userRole === "admin") {
        return [
          { name: "Manage Animals", link: "/admin/manage-animals" },
          { name: "Manage Users", link: "/admin/manage-users" },
        ];
      } else if (userRole === "volunteer") {
        return [{ name: "Volunteer Dashboard", link: "/volunteer/dashboard" }];
      } else {
        return [];
      }
    },
    getUserRole() {
      return localStorage.getItem("userRole") || "guest";
    },
  },
};
</script>
