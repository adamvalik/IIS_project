<template>
    <div class="container mx-auto px-4 py-10">
      <!-- Top Navigation Bar -->
      <header class="flex justify-between items-center bg-blue-500 p-4 text-white rounded-lg shadow-md">
        <h1 class="text-2xl font-bold">DJ Khaled's Animal Shelter</h1>
        <nav>
          <button @click="goToSchedule" class="mr-4 hover:bg-blue-600 py-2 px-4 rounded">Schedule</button>
          <button @click="browseAnimals" class="mr-4 hover:bg-blue-600 py-2 px-4 rounded">Browse Animals</button>
          <button @click="viewProfile" class="hover:bg-blue-600 py-2 px-4 rounded">Profile</button>
        </nav>
      </header>
  
      <!-- Main Content -->
      <main class="mt-6">
        <h2 class="text-xl font-semibold mb-4">Welcome to the Animal Shelter!</h2>
        <p class="text-gray-700">
          We provide a safe haven for animals in need. Explore our services, schedule a visit, or browse our wonderful animals waiting for a home.
        </p>
        <div class="mt-6">
          <button @click="adoptAnimal" class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded">
            Adopt an Animal
          </button>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      goToSchedule() {
        // Redirect to the schedule page
        this.$router.push('/schedule'); // Adjust according to your router setup
      },
      browseAnimals() {
        // Redirect to the browse animals page
        this.$router.push('/browse-animals'); // Adjust according to your router setup
      },
      viewProfile() {
        // Redirect to the user profile page
        this.$router.push('/profile'); // Adjust according to your router setup
      },
      adoptAnimal() {
        // Redirect to the adoption page or modal
        this.$router.push('/adopt'); // Adjust according to your router setup
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any additional styles here if needed */
  .container {
    max-width: 800px;
  }
  </style>
  