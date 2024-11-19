<template>
  <div class="container mx-auto px-4 py-6">
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
            <input v-else v-model="editableAnimal.birth_year" placeholder="Age" type="number" class="text-lg text-gray-600 border border-gray-300 p-2 rounded" />
            </div>

            <div class = "mb-2">
            <p v-if="!editMode" class="text-lg text-gray-600">Size: {{ animal.size }}</p>
            <select
              v-else
              v-model="editableAnimal.size"
              class="text-lg border border-gray-300 p-2 rounded w-full">
              <option value="" disabled>Select size</option>
              <option value="small">small</option>
              <option value="medium">medium</option>
              <option value="large">large</option>
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
          <router-link v-if="this.hasSchedulerPermissions && !editMode" :to="`/scheduler/${animal.id}`" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Schedule</router-link>
          <button v-if="this.hasEditPermissions && !editMode" @click="turnEditMode" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-lg">Edit</button>
          <button v-if="editMode" @click="saveChanges" class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg">Save</button>
          <button v-if="editMode" @click="cancelEdit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg">Cancel</button>
          <h1 v-if="showUnverifiedVolunteer" class="text-lg"><b>You are not verified as a volunteer. Please contact the shelter to verify your volunteer status.</b></h1>
          <button v-if="isCaregiver && !editMode" @click="showVetRequestModal = true" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Medical Request</button>
          <h1 v-if="showUnverifiedVolunteer" class="text-lg"><b>You are not verified as a volunteer. Please contact the shelter to verify your volunteer status.</b></h1>
          <button v-if="!editMode" @click="openHyperlink" class="bg-green-500 hover:bg-red-500 text-white font-bold py-2 px-4 rounded-lg">Contact Us</button>
          <router-link v-if="isCaregiver && !editMode" :to="`/medicalrecords/${animal.id}`" class="bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4 rounded-lg">Medical Records</router-link>
        </div>

        <div v-else class="flex gap-4 items-center">
          <h1 class="text-lg"><b>You are not logged in. To see the pet scheduler, please use the login button at the top of the page or use the sign-up button here:</b></h1>
          <router-link class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0" to="/signup">Sign Up</router-link>
        </div>

        <!-- Vet Request Modal -->
        <div v-if="showVetRequestModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"  @click="showVetModal">
          <div class="bg-white p-6 rounded-lg shadow-lg w-1/2" @click.stop>
            <h2 class="text-2xl font-bold mb-4">Request Specification</h2>
            <textarea v-model="vetRequestText" class="w-full h-40 p-2 border rounded-lg mb-4" placeholder="Enter request details..."></textarea>
            <div class="flex justify-end">
              <button @click="sendVetRequest" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Send Request</button>
            </div>
          </div>
        </div>

        <!-- Request Sent Notification -->
        <div v-if="showRequestSent" class="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg">
          Request Sent
        </div>
        <div v-if="showEmptyRequest" class="fixed bottom-4 right-4 bg-red-500 text-white p-4 rounded-lg shadow-lg">
          Empty request not allowed
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
      showSchedulerModal: false,
      showUnverifiedVolunteer: false,
      hasSchedulerPermissions: false,
      hasEditPermissions: false,
      showVetRequestModal: false,
      vetRequestText: '',
      showRequestSent: false,
      showEmptyRequest: false,
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
    computeBirthYear(newValue) {
      this.editableAnimal.birth_year = new Date().getFullYear() - newValue;
      console.log(this.editableAnimal.birth_year);
    },
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear();
      return currentYear - birthYear;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    turnEditMode(){
      this.editMode = !this.editMode;
    },
    async saveChanges(){
      try {
        await axios.put(`http://localhost:8000/animals/edit/${this.animal.id}`, this.editableAnimal);
        this.animal = { ...this.editableAnimal };
        this.animal.birth_year = new Date().getFullYear() - this.editableAnimal.birth_year;
        this.editMode = false;
      } catch (error) {
        console.error("Error updating animal:", error);
      }
    },
    cancelEdit(){
      this.editMode = false;
    },
    async sendVetRequest() {
      if (this.vetRequestText === '') {
        this.showEmptyRequest = true;
        setTimeout(() => {
          this.showEmptyRequest = false;
        }, 3000);
        return;
      }
      try {
        const response = await axios.post('http://localhost:8000/request', {
          animal_id: this.animal.id,
          caregiver_id: this.user_id,
          request_text: this.vetRequestText
        });
        console.log('Request sent:', response.data);
        this.showVetRequestModal = false;
        this.showRequestSent = true;
        this.vetRequestText = '';
        setTimeout(() => {
          this.showRequestSent = false;
        }, 3000);
      } catch (error) {
        console.error('Error sending request:', error);
      }
    },
    openHyperlink() {
      window.open('https://www.youtube.com/watch?v=AZhWW6URrns', '_blank');
    },
    showVetModal() {
      this.vetRequestText = '';
      this.showVetRequestModal = false;
    }
  }
};
</script>
