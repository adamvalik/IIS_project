<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <div class="mt-10">
      <!-- shelter Info -->
      <section class="mb-10">
        <h2 class="text-3xl font-bold text-gray-800">About Our Shelter</h2>
        <p class="mt-4 text-gray-600">
          Welcome to our Animal Shelter supported by DJ Khaled himself! Our mission is to provide love, care, and a fresh start to animals in need.
          Our dedicated team includes caregivers and veterinarians who work around the clock to ensure each animal’s health, happiness, and well-being.
          <br>
          <strong>Reservations for Walks:</strong> Once verified, visitors can book time to take our animals out for walks!
        </p>
      </section>

      <section class="mb-10">
        <div class="flex justify-between">
          <h3 class="text-2xl font-semibold text-gray-800 mb-6">Recently Added Animals</h3>
          <router-link to="/animals" class="mt-6 block text-blue-500 font-semibold hover:text-blue-600">See all animals</router-link>
        </div>

        <div v-if="loading" class="text-center">Loading...</div>
        <div v-if="!loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <router-link
            v-for="animal in recentAnimals"
            :key="animal.id"
            :to="`/animal/${animal.id}`"
          >
            <AnimalTile
              :name="animal.name"
              :species="animal.species"
              :birth_year="animal.birth_year"
              :photo="animal.photo"
            />
          </router-link>
        </div>
      </section>
    </div>
    <footer class="fixed bottom-0 right-0 text-gray-700 text-sm w-full py-4" style="background-color: #FAF3EB">
      <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <p class="text-center md:text-left">&copy; 2024 DJ Khaled's Animal Shelter. All rights reserved.</p>
        </div>
        <div class="flex gap-4">
          <a href="https://www.instagram.com/djkhaled/" target="_blank" rel="noopener" class="hover:text-blue-500">
            <span class="sr-only">Instagram</span>
            <svg class="w-5 h-5 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M7.5 2h9A5.5 5.5 0 0 1 22 7.5v9a5.5 5.5 0 0 1-5.5 5.5h-9A5.5 5.5 0 0 1 2 16.5v-9A5.5 5.5 0 0 1 7.5 2Zm9 1.5h-9A4 4 0 0 0 3.5 7.5v9a4 4 0 0 0 4 4h9a4 4 0 0 0 4-4v-9a4 4 0 0 0-4-4ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm6.15.9a1.05 1.05 0 1 1-2.1 0 1.05 1.05 0 0 1 2.1 0ZM12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z"/>
            </svg>
          </a>
          <a href="https://x.com/djkhaled" target="_blank" rel="noopener" class="hover:text-blue-500">
            <span class="sr-only">Twitter</span>
            <svg class="w-5 h-5 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.18 4.18 0 0 0 1.84-2.3c-.81.48-1.7.83-2.63 1A4.19 4.19 0 0 0 16.2 4a4.2 4.2 0 0 0-4.15 5.14 11.84 11.84 0 0 1-8.6-4.36A4.2 4.2 0 0 0 5.67 9a4.16 4.16 0 0 1-1.9-.52v.05a4.2 4.2 0 0 0 3.36 4.11c-.46.13-.94.16-1.42.06a4.2 4.2 0 0 0 3.92 2.92A8.38 8.38 0 0 1 2 17.29 11.8 11.8 0 0 0 8.29 19c7.55 0 11.68-6.25 11.68-11.68 0-.18 0-.36-.01-.54A8.3 8.3 0 0 0 22.46 6Z"/>
            </svg>
          </a>
          <a href="https://www.facebook.com/officialdjkhaled" target="_blank" rel="noopener" class="hover:text-blue-500">
            <span class="sr-only">Facebook</span>
            <svg class="w-5 h-5 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M12 2.04a10 10 0 0 0-10 10A10 10 0 0 0 11 21.95v-7.72H8.54V12h2.46v-2.3c0-2.42 1.44-3.75 3.64-3.75.74 0 1.48.06 2.22.14v2.44h-1.52c-1.19 0-1.41.56-1.41 1.38V12h2.74l-.36 2.23H14.9v7.72a10 10 0 0 0 8-9.91 10 10 0 0 0-10-10Z"/>
            </svg>
          </a>
        </div>

      </div>
    </footer>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';
import AnimalTile from '@/components/AnimalTile.vue';
import { mapGetters } from 'vuex';
import apiClient from '@/api';

export default {
  components: {
    NavigationBar,
    AnimalTile,
  },
  data() {
    return {
      recentAnimals: [],
      loading: true,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole']),

    isLoggedIn() {
      return this.isAuthenticated;
    },

    checkListUsersRole() {
      return (this.isAuthenticated && (this.userRole == 'admin' || this.userRole == 'caregiver'));
    },

    checkSchedulerRole() {
      return this.isAuthenticated && this.userRole != 'veterinarian';
    }

  },
  mounted() {
    this.fetchRecentAnimals();
  },
  methods: {
    async fetchRecentAnimals() {
      try {
        const response = await apiClient.get("/animals/recent");
        this.recentAnimals = response.data;
      } catch (error) {
        console.error("Error fetching recent animals:", error);
      } finally {
        this.loading = false;
      }
    },
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear();
      return currentYear - birthYear;
    }
  }
};
</script>
