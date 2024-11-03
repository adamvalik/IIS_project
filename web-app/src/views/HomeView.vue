<template>
  <div class="container mx-auto px-4 py-6">
    <!-- NavigationBar -->
    <NavigationBar />

    <router-link to="/scheduler" v-if="checkSchedulerRole" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-4 inline-block">
      Skibidi Scheduler
    </router-link>
    <!-- <router-link to="/listusers" v-if="checkListUsersRole" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-4 inline-block">
      Skibidi List Users
    </router-link>
    <router-link to="/addanimal" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-4 inline-block">
      Skibidi Add Animal
    </router-link> -->


    <div class="mt-10">
      <!-- Shelter Info -->
      <section class="mb-10">
        <h2 class="text-3xl font-bold text-gray-800">About Our Shelter</h2>
        <p class="mt-4 text-gray-600">
          We are dedicated to providing care and love for abandoned animals. Our shelter works hard to find forever homes for pets and provides resources for adoption, volunteering, and donations.
        </p>
      </section>

      <!-- Last 3 Added Animals -->
      <section class="mb-10">
        <div class="flex justify-between">
          <h3 class="text-2xl font-semibold text-gray-800 mb-6">Recently Added Animals</h3>
          <router-link to="/animals" class="mt-6 block text-blue-500 font-semibold hover:underline">See all animals</router-link>
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
  </div>
</template>

<script>
import axios from 'axios';
import NavigationBar from '@/components/NavigationBar.vue';
import AnimalTile from '@/components/AnimalTile.vue';
import { mapGetters } from 'vuex';

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
        const response = await axios.get("http://localhost:8000/animals/recent");
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
