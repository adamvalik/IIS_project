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
            :isAdmin="isAdmin"
            @toggleDetail="toggleDetail"
            @deleteRecord="deleteRecord"
          />
        </div>
      </div>
    <div v-else>
      <p class="text-gray-700">No medical records for {{this.animal_name}} records found.</p>
    </div>
    <RecordDetail
      v-if="selectedRecord"
      :show="showModal"
      :animalName="animal_name"
      :veterinarianName="selectedRecord.veterinarianName"
      :date="selectedRecord.date"
      :vaccination="selectedRecord.vaccination"
      :description="selectedRecord.description"
      @close="closeModal"
    />
  </div>
</template>


<script>
import axios from 'axios';
import NavigationBar from '@/components/NavigationBar.vue';
import MedicalRecordRow from "@/components/MedicalRecordRow.vue";
import RecordDetail from "@/components/RecordDetail.vue";

export default {
  components: {
    /** eslint-disable */
    MedicalRecordRow,
    NavigationBar,
    RecordDetail,
  },
  data() {
    return {
      records: [],
      selectedRecord: null,
      isCaregiver: false,
      showModal: false,
      animal_id: null,
      animal_name: null,
      isAdmin: this.$store.getters.userRole === 'admin',
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
      console.log(recordId);
      let record = null;
      let veterinarianName = null;
      let animalName = null;

      try {
        const response = await axios.get(`http://localhost:8000/medical_record_get/${recordId}`);
        record = response.data;
        console.log("xxx", record);
        console.log("s",record.id_veterinarian);

      } catch (error) {
        console.error("Error fetching record details:", error);
      }
      if (record) {
        try{
          console.log(record.id_veterinarian);
          const response = await axios.get(`http://localhost:8000/vet/${record.id_veterinarian}`);
          veterinarianName = response.data.name + " " + response.data.surname;
        } catch (error) {
          console.error("Error fetching veterinarian:", error);
        }
        try{
          const response = await axios.get(`http://localhost:8000/animals/animal_name/${record.id_animal}`);
          animalName = response.data;
        } catch (error) {
          console.error("Error fetching animal:", error);
        }
      }
      let vaccination_name = null;
      if (record && record.vaccination){
        vaccination_name = record.vaccination_type;
      }
      this.selectedRecord = {
        veterinarianName: veterinarianName,
        animalName: animalName,
        date: record.date,
        vaccination: vaccination_name,
        description: record.vet_description,
      };
      this.showModal = true;
    },
    deleteRecord(recordId) {
      if (confirm("Are you sure you want to delete this record?")) {
        axios.delete(`http://localhost:8000/medical_record_delete/${recordId}`)
          .then(() => {
            this.fetchMedicalRecords();
          })
          .catch(error => {
            console.error("Error deleting record:", error);
          });
      }
    },
    closeModal() {
      this.showModal = false;
      this.selectedRecord = null;
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
