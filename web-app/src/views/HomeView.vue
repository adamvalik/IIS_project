<template>
  <div class="container mx-auto px-4 py-6">
    <!-- NavigationBar -->
    <NavigationBar />

    <!-- Main Content -->
    <div class="mt-10">
      <!-- Shelter Info -->
      <section class="mb-10">
        <h2 class="text-3xl font-bold text-gray-800">About Our Shelter</h2>
        <p class="mt-4 text-gray-600">We are dedicated to providing care and love for abandoned animals. Our shelter works hard to find forever homes for pets and provides resources for adoption, volunteering, and donations.</p>
      </section>

      <!-- Last 3 Added Animals -->
      <section class="mb-10">
        <h3 class="text-2xl font-semibold text-gray-800 mb-6">Recently Added Animals</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="animal in recentAnimals" :key="animal.id" class="bg-white shadow-md rounded-lg p-6">
            <img :src="animal.image" :alt="animal.name" class="w-full h-48 object-cover rounded-md mb-4" />
            <h4 class="text-xl font-semibold text-gray-700">{{ animal.name }}</h4>
            <p class="text-gray-500 mt-2">Age: {{ animal.age }} years</p>
            <p class="text-gray-500">Type: {{ animal.type }}</p>
          </div>
        </div>
        <router-link to="/animals" class="mt-6 block text-blue-500 font-semibold hover:underline">See all animals</router-link>
      </section>
    </div>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      isLoggedIn: false, // Dynamic check for user login status
      showActions: false, // To control the display of the actions dropdown
      roleActions: [], // Actions based on user role
      recentAnimals: [
        // Mock data for the last 3 added animals (to be fetched from the backend)
        { id: 1, name: "Bella", age: 3, type: "Dog", image: "./assets/puppy.jpg" },
        { id: 2, name: "Max", age: 2, type: "Cat", image: "./assets/kotatko.jpg" },
        { id: 3, name: "Charlie", age: 1, type: "Rabbit", image: "./assets/rabbit.jpg" },
      ],
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
      // Replace this with actual login status logic
      return localStorage.getItem("userToken") !== null;
    },
    getRoleBasedActions() {
      // Fetch actions based on the user's role (mock example)
      const userRole = this.getUserRole(); // Fetch user role dynamically
      if (userRole === "admin") {
        return [
          { name: "Manage Animals", link: "/admin/manage-animals" },
          { name: "Manage Users", link: "/admin/manage-users" },
        ];
      } else if (userRole === "volunteer") {
        return [{ name: "Volunteer Dashboard", link: "/volunteer/dashboard" }];
      } else {
        return []; // Regular users might not have any special actions
      }
    },
    getUserRole() {
      // Mock function to return user role, replace with real logic
      return localStorage.getItem("userRole") || "guest";
    },
  },
};
</script>

<style scoped>
/* Styling for actions dropdown */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {background-color: #f1f1f1}

.dropdown:hover .dropdown-content {
  display: block;
}
</style>
