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
          <option value="dog">Dogs</option>
          <option value="cat">Cats</option>
          <option value="rabbit">Rabbits</option>
        </select>
      </div>

      <div>
        <label for="sort" class="text-gray-700 font-bold mr-2">Sort by:</label>
        <select v-model="sortType" @change="sortAnimals" class="border rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="name">Name</option>
          <option value="age">Age</option>
          <option value="type">Type</option>
        </select>
      </div>
    </section>

     <!-- Animals Grid -->
     <section>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Make each animal card clickable to the detail page -->
        <router-link
          v-for="animal in filteredAnimals"
          :key="animal.id"
          :to="`/animal/${animal.id}`"  
          class="bg-white shadow-md rounded-lg p-6 hover:shadow-xl transition-all"
        >
          <img :src="animal.image || defaultImage" :alt="animal.name" class="w-full h-48 object-cover rounded-md mb-4" />
          <h3 class="text-xl font-semibold text-gray-700">{{ animal.name }}</h3>
          <p class="text-gray-500 mt-2">Age: {{ animal.age }} years</p>
          <p class="text-gray-500">Type: {{ animal.type }}</p>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';


export default {
  components: { 
    NavigationBar
   },
  data() {
    return {
      animals: [
        { id: 1, name: "Bella", age: 3, type: "Dog", image: "./assets/puppy.jpg" },
        { id: 2, name: "Max", age: 2, type: "Cat", image: "./assets/kotatko.jpg" },
        { id: 3, name: "Charlie", age: 1, type: "Rabbit", image: "./assets/rabbit.jpg" },
        { id: 4, name: "Luna", age: 4, type: "Dog", image: "./assets/puppy.jpg" },
        { id: 5, name: "Milo", age: 5, type: "Cat", image: "./assets/kotatko.jpg" },
        { id: 6, name: "Oreo", age: 2, type: "Rabbit", image: "./assets/rabbit.jpg" },
      ],
      filteredAnimals: [],
      filterType: "all",
      sortType: "name",
      defaultImage: "./assets/default-placeholder.png", // Default placeholder image
    };
  },
  mounted() {
    this.filteredAnimals = this.animals;
  },
  methods: {
    filterAnimals() {
      if (this.filterType === "all") {
        this.filteredAnimals = this.animals;
      } else {
        this.filteredAnimals = this.animals.filter((animal) => animal.type.toLowerCase() === this.filterType);
      }
      this.sortAnimals(); // Sort after filtering
    },
    sortAnimals() {
      if (this.sortType === "name") {
        this.filteredAnimals.sort((a, b) => a.name.localeCompare(b.name));
      } else if (this.sortType === "age") {
        this.filteredAnimals.sort((a, b) => a.age - b.age);
      } else if (this.sortType === "type") {
        this.filteredAnimals.sort((a, b) => a.type.localeCompare(b.type));
      }
    },
  },
};
</script>

<style scoped>
/* No additional styling needed for now */
</style>
