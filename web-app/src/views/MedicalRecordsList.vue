<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 v-if="isCaregiver" class="mb-4 text-3xl font-bold text-gray-800 py-8">List Medical Records</h2>

    <h3 class="text-xl font-semibold text-gray-700 mb-4">Medical Records for {{this.animal_name}}</h3>
    <div v-if="records.length">
        <div class="grid grid-cols-1">
          <MedicalRecordRow
            v-for="record in records"
            :key="record.id"
            :animal_name="animal_name"
            :record="record"
            @toggleDetail="toggleDetail"
          />
        </div>
      </div>
    <div v-else>
      <p class="text-gray-700">No medical for {{this.animal_name}} records found.</p>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import NavigationBar from '@/components/NavigationBar.vue';
import MedicalRecordRow from "@/components/MedicalRecordRow.vue";

export default {
  components: {
    /** eslint-disable */
    MedicalRecordRow,
    NavigationBar,
  },
  data() {
    return {
      records: [],
      selectedRecord: null,
      isCaregiver: false,
      animal_id: null,
      animal_name: null
    };
  },
  computed: {
    // medicalRecords() {
    //   // const currentDate = new Date();
    //   // return this.reservations.filter(
    //   //   reservation => new Date(reservation.borrow.date) < currentDate
    //   // );
    // },
  },
  async created() {
    this.animal_id = this.$route.params.id;
    this.isCaregiver = this.$store.getters.userRole === 'caregiver' || this.$store.getters.userRole === 'admin';
    this.isVolunteer = this.$store.getters.userRole === 'volunteer';
    await this.fetchMedicalRecords();
    await this.fetchAnimalName();
  },
  methods: {
    async fetchMedicalRecords() {
      try {
          console.log(this.animal_id);
          const response = await axios.get(`http://localhost:8000/medical_records/${this.animal_id}`);
          this.records = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async toggleDetail(recordId) {
      try {
        if (!recordId) {
          console.error('No reservation ID provided');
          return;
        }
        await axios.put(`http://localhost:8000/reservations/${recordId}/toggle_borrowed`);
        await this.fetchMedicalRecords();
      } catch (error) {
        console.error('Error toggling borrowed:', error);
      }
    },
    async fetchAnimalName() {
      try {
        const response = await axios.get(`http://localhost:8000/animals/animal_name/${this.animal_id}`);
        this.animal_name = response.data;
      } catch (error) {
        console.error("Error fetching animal:", error);
      }
    },
  },
};
</script>
