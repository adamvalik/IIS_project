<template>
  <div class="container mx-auto px-4 py-10">
    <!-- Hero Section -->
    <section class="hero bg-cover bg-center py-20 mb-10" style="background-image: url('./assets/shelter-banner.jpg')">
      <div class="text-center text-gray-700">
        <h1 class="text-5xl font-bold mb-6">Welcome to the Animal Shelter</h1>
        <p class="text-lg mb-10">Adopt, Volunteer, or Donate to help our animals find loving homes.</p>
        <div class="flex justify-center space-x-4">
          <router-link to="/adopt" class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg">Adopt a Pet</router-link>
          <router-link to="/volunteer" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg">Volunteer</router-link>
          <router-link to="/donate" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg">Donate</router-link>
          <router-link to="/scheduler" class="bg-purple-500 hover:bg-purple-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg">Open Scheduler</router-link>
        </div>
      </div>
    </section>

    <!-- Animal Filters -->
    <section class="text-center mb-10">
      <h2 class="text-3xl font-semibold text-gray-800 mb-4">Meet Our Animals</h2>
      <div class="flex justify-center space-x-6">
        <button @click="filterAnimals('all')" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-6 rounded-lg">All</button>
        <button @click="filterAnimals('dog')" class="bg-green-200 hover:bg-green-300 text-green-800 font-bold py-2 px-6 rounded-lg">Dogs</button>
        <button @click="filterAnimals('cat')" class="bg-blue-200 hover:bg-blue-300 text-blue-800 font-bold py-2 px-6 rounded-lg">Cats</button>
        <button @click="filterAnimals('rabbit')" class="bg-yellow-200 hover:bg-yellow-300 text-yellow-800 font-bold py-2 px-6 rounded-lg">Rabbits</button>
      </div>
    </section>

    <!-- Animal Cards with Hover Effects -->
    <section>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="animal in filteredAnimals"
          :key="animal.id"
          class="relative group bg-white shadow-md rounded-lg p-6 hover:shadow-xl transition-all"
        >
          <img :src="animal.image || defaultImage" :alt="animal.name" class="w-full h-48 object-cover rounded-md mb-4" />
          <h3 class="text-xl font-semibold text-gray-700">{{ animal.name }}</h3>
          <p class="text-gray-600">{{ animal.description }}</p>
          <p class="text-gray-500 mt-2">Age: {{ animal.age }} years</p>
          <p class="text-gray-500">Type: {{ animal.type }}</p>

          <!-- Hover Details -->
          <div class="absolute inset-0 bg-black bg-opacity-50 text-white flex flex-col justify-center items-center opacity-0 group-hover:opacity-100 transition-opacity">
            <h3 class="text-2xl">{{ animal.name }}</h3>
            <p class="mt-2">{{ animal.age }} years old, {{ animal.type }}</p>
            <router-link :to="`/adopt/${animal.id}`" class="mt-4 bg-green-500 hover:bg-green-600 py-2 px-4 rounded-lg text-white">Adopt {{ animal.name }}</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="bg-gray-100 py-12 mt-20">
      <h2 class="text-center text-3xl font-semibold text-gray-800 mb-8">Happy Adoption Stories</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-white shadow-md rounded-lg p-6">
          <p class="italic text-gray-600">"Adopting Bella was the best decision of our lives! She's the most loving dog and has become a part of our family."</p>
          <p class="mt-4 text-gray-800 font-bold">- John Doe</p>
        </div>
        <div class="bg-white shadow-md rounded-lg p-6">
          <p class="italic text-gray-600">"Max has brought so much joy into our lives. We're grateful to the shelter for helping us find our new family member."</p>
          <p class="mt-4 text-gray-800 font-bold">- Jane Smith</p>
        </div>
        <div class="bg-white shadow-md rounded-lg p-6">
          <p class="italic text-gray-600">"Charlie the rabbit is the sweetest! We can't thank the shelter enough for all they do."</p>
          <p class="mt-4 text-gray-800 font-bold">- Emma Brown</p>
        </div>
      </div>
    </section>

    <!-- Newsletter Signup Section -->
    <section class="bg-gray-100 text-gray-700 py-12 mt-20 text-center">
      <h2 class="text-3xl font-semibold mb-6">Stay Updated</h2>
      <p class="mb-8">Subscribe to our newsletter to get updates on new arrivals and upcoming events!</p>
      <form @submit.prevent="submitNewsletter" class="flex justify-center">
        <input v-model="email" type="email" placeholder="Enter your email" class="text-gray-800 py-3 px-6 rounded-l-lg focus:outline-none" />
        <button type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-6 rounded-r-lg">Subscribe</button>
      </form>
    </section>

    <!-- Footer Section -->
    <footer class="bg-gray-100 text-gray-700 py-10 mt-20">
      <div class="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-10">
        <div>
          <h3 class="text-lg font-bold">Contact Us</h3>
          <p class="mt-4">123 Animal Shelter Road, Townsville</p>
          <p>Email: contact@animalshelter.org</p>
          <p>Phone: (123) 456-7890</p>
        </div>
        <div>
          <h3 class="text-lg font-bold">Quick Links</h3>
          <ul class="mt-4 space-y-2">
            <li><router-link to="/adopt" class="hover:underline">Adopt a Pet</router-link></li>
            <li><router-link to="/volunteer" class="hover:underline">Volunteer</router-link></li>
            <li><router-link to="/donate" class="hover:underline">Donate</router-link></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-bold">Follow Us</h3>
          <div class="flex space-x-4 mt-4">
            <a href="#"><i class="fab fa-facebook text-2xl"></i></a>
            <a href="#"><i class="fab fa-instagram text-2xl"></i></a>
            <a href="#"><i class="fab fa-twitter text-2xl"></i></a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      animals: [
        { id: 1, name: "Bella", description: "A playful dog.", age: 3, type: "Dog", image: "./assets/puppy.jpg" },
        { id: 2, name: "Max", description: "A friendly cat.", age: 2, type: "Cat", image: "./assets/kotatko.jpg" },
        { id: 3, name: "Charlie", description: "A gentle rabbit.", age: 1, type: "Rabbit", image: "./assets/rabbit.jpg" },
      ],
      filteredAnimals: [],
      selectedFilter: "all",
      email: "",
      defaultImage: "./assets/default-placeholder.png",
    };
  },
  mounted() {
    this.filteredAnimals = this.animals;
  },
  methods: {
    filterAnimals(type) {
      this.selectedFilter = type;
      if (type === "all") {
        this.filteredAnimals = this.animals;
      } else {
        this.filteredAnimals = this.animals.filter((animal) => animal.type.toLowerCase() === type.toLowerCase());
      }
    },
    submitNewsletter() {
      console.log("Email submitted:", this.email);
      // Add your newsletter subscription logic here
    },
  },
};
</script>

<style scoped>
.hero {
  background-size: cover;
  background-position: center;
  min-height: 400px;
}

.loader {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
