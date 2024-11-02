<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Include the NavigationBar component -->
    <NavigationBar />

    <!-- Filters and Sorting -->
    <section class="flex gap-4 items-center py-4">
      <div>
        <label for="filter" class="text-gray-700 font-bold mr-2">Filter by:</label>
        <select v-model="filterType" @change="fetchAnimals" class="border rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="all">All</option>
          <option v-for="species in uniqueSpecies" :key="species" :value="species.toLowerCase()">
            {{ species }}
          </option>
        </select>
      </div>

      <div>
        <label for="sort" class="text-gray-700 font-bold mr-2">Sort by:</label>
        <select v-model="sortType" @change="fetchAnimals" class="border rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="name">Name</option>
          <option value="age">Age</option>
          <option value="species">Species</option>
        </select>
      </div>
    </section>

    <div v-if="loading" class="text-center">Loading...</div>
    <section v-if="!loading">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          v-for="animal in animals"
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
</template>

<script>
import AnimalTile from '@/components/AnimalTile.vue';
import NavigationBar from '@/components/NavigationBar.vue';
import axios from 'axios';

export default {
  components: {
    NavigationBar,
    AnimalTile
  },
  data() {
    return {
      animals: [],
      filterType: "all",
      sortType: "name",
      uniqueSpecies: [],
      loading: true,
    };
  },
  async mounted() {
    await this.fetchAnimals();
    this.extractSpecies();
  },
  methods: {
    async fetchAnimals() {
      try {
        const params = {
          filter: this.filterType !== "all" ? this.filterType : undefined,
          sort: this.sortType,
        };
        const response = await axios.get("http://localhost:8000/animals/", { params });
        this.animals = response.data;
      } catch (error) {
        console.error("Error fetching animals:", error);
      } finally {
        this.loading = false;
      }
    },
    async extractSpecies() {
      try {
        const response = await axios.get("http://localhost:8000/animals/species");
        this.uniqueSpecies = response.data;
      } catch (error) {
        console.error("Error fetching species:", error);
      }
    },
  },
};
</script>
