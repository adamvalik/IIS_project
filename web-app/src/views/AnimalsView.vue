<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Include the NavigationBar component -->
    <NavigationBar />

    <!-- Filters and Sorting -->
    <section class="flex gap-4 items-center py-4">
      <div>
        <label for="filter" class="text-gray-700 font-bold mr-2">Filter by:</label>
        <select v-model="filterType" @change="filterAnimals" class="border rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="all">All</option>
          <!-- Dynamically generate options based on species -->
          <option v-for="species in uniqueSpecies" :key="species" :value="species.toLowerCase()">
            {{ species }}
          </option>
        </select>
      </div>

      <div>
        <label for="sort" class="text-gray-700 font-bold mr-2">Sort by:</label>
        <select v-model="sortType" @change="sortAnimals" class="border rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="name">Name</option>
          <option value="age">Age</option>
          <option value="species">Species</option>
        </select>
      </div>
    </section>

    <!-- Animals Grid -->
    <section>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Use AnimalTile component -->
        <router-link
          v-for="animal in filteredAnimals"
          :key="animal.id"
          :to="`/animal/${animal.id}`"
        >
          <AnimalTile
            :name="animal.name"
            :species="animal.species" 
            :birth_year="animal.birth_year"
            :photo="animal.photo || defaultImage"
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
      filteredAnimals: [],
      filterType: "all",
      sortType: "name",
      defaultImage: "./assets/default.png", 
      uniqueSpecies: [],  // Dynamic species list
    };
  },
  async mounted() {
    await this.fetchAnimals();
    this.filterAnimals();
  },
  methods: {
    async fetchAnimals() {
      try {
        const response = await axios.get('http://localhost:8000/animals');
        this.animals = response.data;
        this.filteredAnimals = this.animals;
        this.extractSpecies(); // Extract unique species from the fetched data
      } catch (error) {
        console.error('Error fetching animals:', error);
      }
    },
    extractSpecies() {
      const speciesSet = new Set(this.animals.map(animal => animal.species));
      this.uniqueSpecies = Array.from(speciesSet); // Create an array of unique species
    },
    filterAnimals() {
      if (this.filterType === "all") {
        this.filteredAnimals = this.animals;
      } else {
        this.filteredAnimals = this.animals.filter((animal) => animal.species.toLowerCase() === this.filterType);
      }
      this.sortAnimals(); // Sort after filtering
    },
    sortAnimals() {
      if (this.sortType === "name") {
        this.filteredAnimals.sort((a, b) => a.name.localeCompare(b.name));
      } else if (this.sortType === "age") {
        this.filteredAnimals.sort((a, b) => a.age - b.age);
      } else if (this.sortType === "type") {
        this.filteredAnimals.sort((a, b) => a.species.localeCompare(b.species));
      }
    },
  },
};
</script>

<style scoped>
/* No additional styling needed for now */
</style>
