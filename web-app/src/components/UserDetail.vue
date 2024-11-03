<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <div class="bg-white shadow-lg rounded-lg p-8">
      <div class="flex flex-col gap-8">
        <div class="flex flex-col md:flex-row items-center md:space-x-8">

          <div class="mt-6 md:mt-0">
            <h2 class="text-3xl font-bold text-gray-800 mb-4">{{ user.name }}</h2>
            <p class="text-lg text-gray-600 mb-2">Surname: {{ user.surname }}</p>
            <p class="text-lg text-gray-600 mb-2">E-Mail: {{ user.mail }}</p>
            <p class="text-lg text-gray-600 mb-2">Telephone Number: {{ user.telephone }} years</p>
            <p class="text-lg text-gray-600 mb-2">Role: {{ user.role }}</p>
          </div>
        </div>

        <div v-if="isAuthenticated" class="flex gap-4">
          <router-link v-if="this.hasSchedulerPermissions" to="/scheduler" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Schedule</router-link>
          <h1 v-if="showUnverifiedVolunteer" class="text-lg"><b>You are not verified as a volunteer. Please contact the shelter to verify your volunteer status.</b></h1>
          <button v-if="isCaregiver" @click="showVetRequestModal = true" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Medical Request</button>
          <h1 v-if="showUnverifiedVolunteer" class="text-lg"><b>You are not verified as a volunteer. Please contact the shelter to verify your volunteer status.</b></h1>
          <button @click="openHyperlink" class="bg-green-500 hover:bg-red-500 text-white font-bold py-2 px-4 rounded-lg">Contact Us</button>
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
      user: {},
      showSchedulerModal: false,
      showUnverifiedVolunteer: false,
      hasSchedulerPermissions: false,
      showVetRequestModal: false,
      vetRequestText: '',
      showRequestSent: false,
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
    isCaregiver() {
      return this.userRole === 'caregiver';
    },
  },
  async mounted() {
    const animalId = this.$route.params.id;
    this.fetchAnimal(animalId);
    this.loadSchedulerPermissions(this.user_id);
  },
  methods: {
    async fetchUser(id) {
      try {
        const response = await axios.post('http://localhost:8000/user_detail',
          {
            id: id
          });
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching recent animals:", error);
      }
    },
    async loadSchedulerPermissions(userId) {

      if (this.isAuthenticated) {
        this.hasSchedulerPermissions = true;

        if (this.userRole === 'veterinarian') {
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
    }
  }
};
</script>
