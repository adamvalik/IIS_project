<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <div class="bg-white shadow-lg rounded-lg p-8">
      <div class="flex flex-col md:flex-row items-center md:space-x-8">
        <!-- Animal Image -->
        <img :src="animal.photo || defaultImage" :alt="animal.name" class="w-full md:w-1/3 h-64 object-cover rounded-lg shadow-md" />

        <!-- Animal Info -->
        <div class="mt-6 md:mt-0">
          <h2 class="text-3xl font-bold text-gray-800 mb-4">{{ animal.name }}</h2>
          <p class="text-lg text-gray-600 mb-2">Species: {{ animal.species }}</p>
          <p class="text-lg text-gray-600 mb-2">Breed: {{ animal.breed }}</p>
          <p class="text-lg text-gray-600 mb-2">Age: {{ calculateAge(animal.birth_year) }} years</p>
          <p class="text-lg text-gray-600 mb-2">Size: {{ animal.size }}</p>
          <p class="text-lg text-gray-600 mb-2">Admission Date: {{ formatDate(animal.admission_date) }}</p>
          <p class="text-lg text-gray-600">{{ animal.description }}</p>

          <!-- Role-based actions -->
          <div class="mt-6">
            <button
              v-if="isAdmin"
              @click="editAnimal"
              class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mr-4"
            >
              Edit Animal
            </button>
            <button
              v-if="isUser"
              @click="adoptAnimal"
              class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg"
            >
              Adopt {{ animal.name }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavigationBar from './NavigationBar.vue';

export default {
  components: { 
    NavigationBar
  },
  data() {
    return {
      animal: {}, // This will be populated via API call
      defaultImage: '/assets/default.png',
      isAdmin: true,
      isUser: true,
    };
  },
  async mounted() {
    const animalId = this.$route.params.id;
    try {
      // Fetch the animal details using the animal ID
      const response = await fetch(`http://localhost:8000/animal/${animalId}`);
      this.animal = await response.json();
    } catch (error) {
      console.error("Error fetching animal details:", error);
    }
  },
  methods: {
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear();
      return currentYear - birthYear;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString(); // Formats date to "MM/DD/YYYY"
    },
    editAnimal() {
      // Logic for editing animal (admin action)
      console.log('Edit animal', this.animal.id);
    },
    adoptAnimal() {
      // Logic for adopting the animal (user action)
      console.log('Adopt animal', this.animal.id);
    },
  },
};
</script>

<style scoped>
/* Styling for animal details */
</style>
