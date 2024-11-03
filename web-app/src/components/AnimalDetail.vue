<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <div class="bg-white shadow-lg rounded-lg p-8">
      <div class="flex flex-col gap-8">
        <div class="flex flex-col md:flex-row items-center md:space-x-8">
          <img :src="animal.photo" :alt="animal.name" class="w-full md:w-1/3 h-64 object-cover rounded-lg shadow-md" />

          <div class="mt-6 md:mt-0">
            <div class = "mb-4">
            <h2 v-if="!editMode" class="text-3xl font-bold text-gray-800">{{ animal.name }}</h2>
            <input v-else v-model="editableAnimal.name" placeholder="Name" class="text-3xl font-bold text-gray-800 border border-gray-300 p-2 rounded" />
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600">Species: {{ animal.species }}</p>
            <input v-else v-model="editableAnimal.species" placeholder="species" class="text-lg text-gray-600 border border-gray-300 p-2 rounded" />
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600">Breed: {{ animal.breed }}</p>
            <input v-else v-model="editableAnimal.breed" placeholder="breed" class="text-lg text-gray-600 border border-gray-300 p-2 rounded" />
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600">Age: {{ calculateAge(animal.birth_year) }} years</p>
            <input v-else v-model="editableAnimal.birth_year" placeholder="age" type="number" class="text-lg text-gray-600 border border-gray-300 p-2 rounded" />
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600">Size: {{ animal.size }}</p>
            <select 
              v-else 
              v-model="editableAnimal.size" 
              class="text-lg border border-gray-300 p-2 rounded w-full">
              <option value="" disabled>Select size</option>
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="big">Big</option>
            </select>
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600 mb-2">Admission Date: {{ formatDate(animal.admission_date) }}</p>
            <input v-else v-model="editableAnimal.admission_date" placeholder="admission date" type="date" class="text-lg text-gray-600 border border-gray-300 p-2 rounded" />
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600">{{ animal.caregivers_description }}</p>
            <textarea v-else v-model="editableAnimal.caregivers_description" placeholder="caregivers description" class="text-lg text-gray-600 border border-gray-300 p-2 rounded"></textarea>
            </div>
          
          </div>
        </div>
        <div v-if="isAuthenticated" class="flex gap-4">
          <router-link v-if="this.hasSchedulerPermissions && !editMode" to="/scheduler" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Schedule</router-link>
          <button v-if="this.hasEditPermissions && !editMode" @click="turnEditMode" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-lg">Edit</button>
          <button v-if="editMode" @click="saveChanges" class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg">Save</button>
          <button v-if="editMode" @click="cancelEdit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg">Cancel</button>
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
      editableAnimal: {},
      editMode: false,
      showUnverifiedVolunteer: false,
      hasSchedulerPermissions: false,
      hasEditPermissions: false,
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
    this.loadEditPermissions();
  },
  methods: {
    async fetchAnimal(id) {
      try {
        const response = await axios.get(`http://localhost:8000/animals/animal/${id}`);
        this.animal = response.data;
        this.editableAnimal = { ...this.animal };
      } catch (error) {
        console.error("Error fetching recent animals:", error);
      }
    },
    async loadEditPermissions() {
      if (this.isAuthenticated) {
        if (this.userRole === 'admin' || this.userRole === 'caregiver') {
          this.hasEditPermissions = true;
        }
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
    turnEditMode(){
      this.editMode = !this.editMode;
    },
    async saveChanges(){
      try {
        await axios.put(`http://localhost:8000/animals/edit/${this.animal.id}`, this.editableAnimal);
        this.animal = { ...this.editableAnimal };
        this.editMode = false;
      } catch (error) {
        console.error("Error updating animal:", error);
      }
    },
    cancelEdit(){
      this.editMode = false;
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
