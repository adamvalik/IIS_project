<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <div class="bg-white shadow-lg rounded-lg p-8">
      <div class="flex flex-col gap-8">
        <div class="flex flex-col md:flex-row items-center md:space-x-8">
          <img :src="animal.photo" :alt="animal.name" class="w-full md:w-1/3 h-64 object-cover rounded-lg shadow-md" />

          <div class="mt-6 md:mt-0">
            <h2 class="text-3xl font-bold text-gray-800 mb-4">{{ animal.name }}</h2>
            <p class="text-lg text-gray-600 mb-2">Species: {{ animal.species }}</p>
            <p class="text-lg text-gray-600 mb-2">Breed: {{ animal.breed }}</p>
            <p class="text-lg text-gray-600 mb-2">Age: {{ calculateAge(animal.birth_year) }} years</p>
            <p class="text-lg text-gray-600 mb-2">Size: {{ animal.size }}</p>
            <p class="text-lg text-gray-600 mb-2">Admission Date: {{ formatDate(animal.admission_date) }}</p>
            <p class="text-lg text-gray-600">{{ animal.caregivers_description }}</p>
          </div>
        </div>
        <div class="flex gap-4">
          <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Volunteer</button>
          <button class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Please wait for verification</button>
          <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Schedule</button>
          <button class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Edit</button>
          <button class="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Show Medical Records</button>
          <button class="bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Create Vet Request</button>
          <button class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0">Contact</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavigationBar from './NavigationBar.vue';
import axios from 'axios';

export default {
  components: {
    NavigationBar
  },
  data() {
    return {
      animal: {},
    };
  },
  async mounted() {
    const animalId = this.$route.params.id;
    this.fetchAnimal(animalId);
  },
  methods: {
    async fetchAnimal(id) {
      try {
        const response = await axios.get(`http://localhost:8000/animals/animal/${id}`);
        this.animal = response.data;
      } catch (error) {
        console.error("Error fetching recent animals:", error);
      }
    },
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear();
      return currentYear - birthYear;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
  },
};
</script>
