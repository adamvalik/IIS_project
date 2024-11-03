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
        <div v-if="isAuthenticated" class="flex gap-4">
          <router-link v-if="this.hasSchedulerPermissions" to="/scheduler" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Schedule</router-link>
          <h1 v-if="showUnverifiedVolunteer" class="text-lg"><b>You are not verified as a volunteer. Please contact the shelter to verify your volunteer status.</b></h1>
        </div>
        
        <div v-else class="flex gap-4 items-center">
          <h1 class="text-lg"><b>You are not logged in. To see the pet scheduler, please use the login button at the top of the page or use the sign-up button here:</b></h1>
          <router-link class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0" to="/signup">Sign Up</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavigationBar from './NavigationBar.vue';
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  components: {
    NavigationBar
  },
  data() {
    return {
      animal: {},
      showUnverifiedVolunteer: false,
      hasSchedulerPermissions: false,
    };
  },
  computed: {
  ...mapGetters(['isAuthenticated', 'userRole', 'user_id']),

    isLoggedIn() {
      return this.isAuthenticated;
    },
    isVeterinarian() {
      return this.userRole === 'veterinarian';
    },
  },
  async mounted() {
    const animalId = this.$route.params.id;
    this.fetchAnimal(animalId);
    this.loadSchedulerPermissions(this.user_id);
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
    async loadSchedulerPermissions(userId) {

      if(this.isAuthenticated){
        this.hasSchedulerPermissions = true;

        if(this.userRole === 'veterinarian'){
          this.hasSchedulerPermissions = false;
        }
        if (this.userRole === 'volunteer') {
          console.log("User is a volunteer");
          console.log("User ID: ", userId);
          try {
            const response = await axios.get(`http://localhost:8000/users/volunteers/${userId}/verify`);
            if (response.data === true) {
              console.log("User is verified");
              this.VolunteerVetification = true;
            } else {
              console.log("User is not verified");
              this.showUnverifiedVolunteer = true;
              this.hasSchedulerPermissions = false;
            }
          } catch (error) {
            console.error("Error fetching user permissions:", error);
            this.hasSchedulerPermissions = false;
            this.VolunteerVetification = false;
          }
        }
      }
    },
    // async loadVolunteerVetification() {
    //   if (this.isAuthenticated && this.userRole === 'volunteer') {
    //     try {
    //       const response = await axios.get('http://localhost:8000/users/volunteers/${this.$store.getters.userId}');
    //       if (response.data === 'true') {
    //         return true;
    //       }
    //     } catch (error) {
    //       console.error("Error fetching user verification:", error);
    //       return false;
    //     }
    //   }
    // },
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
