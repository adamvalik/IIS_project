<template>
  <div class="container mx-auto px-4 py-6">
    <NavigationBar class="mb-4" />

    <div class="bg-white shadow-lg rounded-lg p-8">
      <div class="flex flex-col gap-8">
        <div class="flex flex-col md:flex-row items-center md:space-x-8 overflow-">
          <img
            :src="animal.photo || '/assets/placeholder.png'"
            alt="Photo"
            loading="lazy"
            class="w-full md:w-1/3 h-64 object-cover rounded-lg shadow-md self-start"
          />

          <div class="mt-6 md:mt-0">
            <div>
              <h2 v-if="!editMode" class="mb-4 text-3xl font-bold text-gray-800">{{ animal.name }}</h2>
              <input v-else v-model="editableAnimal.name" placeholder="Name" class="text-gray-800 border border-gray-300 p-2 rounded w-full" />
            </div>

            <div>
              <p v-if="!editMode" class="mb-2 text-lg text-gray-600">Species: {{ animal.species }}</p>
              <input v-else v-model="editableAnimal.species" placeholder="species" class="text-gray-600 border border-gray-300 p-2 rounded w-full" />
            </div>

            <div>
              <p v-if="!editMode" class="mb-2 text-lg text-gray-600">Breed: {{ animal.breed }}</p>
              <input v-else v-model="editableAnimal.breed" placeholder="breed" class="text-gray-600 border border-gray-300 p-2 rounded w-full" />
            </div>

            <div>
              <p v-if="!editMode" class="mb-2 text-lg text-gray-600">Age: {{ calculateAge(animal.birth_year) }} years</p>
              <input v-else v-model="editableAnimal.birth_year" placeholder="Age" type="number" class=" text-gray-600 border border-gray-300 p-2 rounded w-full" />
            </div>

            <div>
              <p v-if="!editMode" class="mb-2 text-lg text-gray-600">Size: {{ animal.size }}</p>
              <select
                v-else
                v-model="editableAnimal.size"
                class="border border-gray-300 p-2 rounded w-full">
                <option value="" disabled>Select size</option>
                <option value="small">small</option>
                <option value="medium">medium</option>
                <option value="large">large</option>
              </select>
            </div>

            <div>
              <p v-if="!editMode" class="text-lg text-gray-600 mb-2">Admission Date: {{ formatDate(animal.admission_date) }}</p>
              <input v-else v-model="editableAnimal.admission_date" placeholder="admission date" type="date" class="text-gray-600 border border-gray-300 p-2 rounded w-full" />
            </div>

            <div>
              <p v-if="!editMode" class="mb-2 text-lg text-gray-600 break-words">{{ animal.caregivers_description }}</p>
              <textarea v-else v-model="editableAnimal.caregivers_description" placeholder="caregivers description" rows="1" class="text-gray-600 border border-gray-300 p-2 rounded w-full"></textarea>
            </div>
          </div>
        </div>

        <!-- buttons -->
        <div v-if="isAuthenticated && !isDeleted" class="flex gap-4">
          <router-link
            v-if="this.hasSchedulerPermissions && !editMode"
            :to="`/scheduler/${animal.id}`"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Walking Schedule
          </router-link>
          <button
            v-if="editMode"
            @click="saveChanges"
            class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Save
          </button>
          <button
            v-if="editMode"
            @click="cancelEdit"
            class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Cancel
          </button>
          <h1
            v-if="showUnverifiedVolunteer"
            class="text-lg"
          >
            <b>You are not verified as a volunteer. Please contact the shelter to verify your volunteer status.</b>
          </h1>
          <button
            v-if="isCaregiver && !editMode"
            @click="showVetRequestModal = true"
            class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Examination Request
          </button>
          <router-link
            v-if="(isCaregiver || isAdmin || isVeterinarian) && !editMode"
            :to="`/medicalrecords/${animal.id}`"
            class="bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Medical Records
          </router-link>
          <button
            v-if="this.hasEditPermissions && !editMode"
            @click="turnEditMode"
            class="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Edit Animal
          </button>

          <button
            v-if="(isCaregiver || isAdmin) && !editMode"
            @click="deleteAnimal"
            class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Delete Animal
          </button>
        </div>

        <div v-if="!isAuthenticated && !isDeleted" class="flex gap-4 items-center">
          <h1 class="text-md text-gray-500">To see the pet scheduler, please use the login button at the top of the page or use the sign-up button here:</h1>
          <router-link
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg mt-6 md:mt-0"
            to="/signup"
          >
            Sign Up
          </router-link>
        </div>

        <!-- examination request modal -->
        <div v-if="showVetRequestModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"  @click="showVetModal">
          <div class="bg-white p-6 rounded-lg shadow-lg w-1/2" @click.stop>
            <h2 class="text-2xl font-bold mb-4">Request Specification</h2>
            <textarea v-model="vetRequestText" class="w-full h-40 p-2 border rounded-lg mb-4" placeholder="Enter request details..."></textarea>
            <div class="flex justify-end">
              <button @click="sendVetRequest" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Send Request</button>
            </div>
          </div>
        </div>

        <!-- notifications -->
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
import apiClient from '@/api';
import NavigationBar from '@/components/NavigationBar.vue';
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
      isDeleted: false,
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
    isAdmin() {
      return this.userRole === 'admin';
    },
  },
  async mounted() {
    const animalId = this.$route.params.id;
    this.fetchAnimal(animalId);
    this.fetchIsDeleted(animalId);
    this.loadSchedulerPermissions(this.user_id);
    this.loadEditPermissions();
  },

  methods: {
    async fetchAnimal(id) {
      try {
        const response = await apiClient.get(`/animals/animal/${id}`);
        this.animal = response.data;
        this.editableAnimal = { ...this.animal };
      } catch (error) {
        console.error("Error fetching recent animals:", error);
      }
    },
    async fetchIsDeleted(id) {
      try {
        const response = await apiClient.get(`/animals/${id}/is_deleted`);
        this.isDeleted = response.data;
        if (this.isDeleted) {
          alert('Animal has been deleted');
          this.$router.go(-1);
        }
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
            const response = await apiClient.get(`/users/volunteers/${userId}/verify`, {
                headers: {
                  Authorization: `Bearer ${this.$store.state.accessToken}`,
                }
              }
            );
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
      this.editableAnimal.birth_year = new Date().getFullYear() - this.animal.birth_year;
    },
    async saveChanges(){
      try {
        this.editableAnimal.birth_year = new Date().getFullYear() - this.editableAnimal.birth_year;
        await apiClient.put(`/animals/edit/${this.animal.id}`,
          this.editableAnimal,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            }
          });
        this.animal = { ...this.editableAnimal };
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
        const response = await apiClient.post('/request', {
          animal_id: this.animal.id,
          caregiver_id: this.user_id,
          request_text: this.vetRequestText
        }, {
          headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`,
          },
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
    showVetModal() {
      this.vetRequestText = '';
      this.showVetRequestModal = false;
    },
    async deleteAnimal() {
      if (confirm('Are you sure you want to delete this animal?')) {
        try {
          await apiClient.delete(`/animals/delete/${this.animal.id}`, {
            headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
            }
          });
          this.$router.go(-1);
        } catch (error) {
          console.error('Error deleting animal:', error);
        }
      }
    }
  }
};
</script>
