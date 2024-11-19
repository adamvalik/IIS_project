<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 v-if="isCaregiver" class="mb-4 text-3xl font-bold text-gray-800 py-8">List Medical Records</h2>

    <h3 v-if="animal_id" class="text-xl font-semibold text-gray-700 mb-4">Medical Records for {{animal_name}}</h3>
    <h3 v-else class="text-xl font-semibold text-gray-700 mb-4">All Medical Records</h3>
    <div v-if="records.length">
      <div class="grid grid-cols-1">
        <MedicalRecordRow
          v-for="record in records"
          :key="record.id"
          :showAnimalName="animal_id"
          :animal_name="record.animal_name"
          :record="record"
          :isAdmin="isAdmin"
          @toggleDetail="toggleDetail"
          @deleteRecord="deleteRecord"
        />
      </div>
    </div>
    <div v-else>
      <p v-if="animal_id" class="text-gray-700">No medical records for {{animal_name}} records found.</p>
      <p v-else class="text-gray-700">No medical records found.</p>
    </div>
    <RecordDetail
      v-if="selectedRecord"
      :show="showModal"
      :animalName="selectedRecord.animal_name"
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
  async created() {
    this.animal_id = this.$route.params.id;
    console.log(this.animal_id);
    this.isCaregiver = this.$store.getters.userRole === 'caregiver' || this.$store.getters.userRole === 'admin';
    this.isVolunteer = this.$store.getters.userRole === 'volunteer';
    await this.fetchMedicalRecords();
    this.animal_name = await this.fetchAnimalName(this.animal_id);
  },
  methods: {
    async fetchMedicalRecords() {
      if (!this.animal_id) {
        //fetch all
        try {
          const response = await axios.get(`http://localhost:8000/all_medical_records`);
          this.records = response.data;
          for (let record of this.records) {
            record.animal_name = await this.fetchAnimalName(record.id_animal);
          }
        } catch (error) {
          console.error(error);
        }
      }
      else {
        try {
          console.log(this.animal_id);
          const response = await axios.get(`http://localhost:8000/medical_records/${this.animal_id}`);
          this.records = response.data;
          for (let record of this.records) {
            record.animal_name = await this.fetchAnimalName(record.id_animal);
          }
        } catch (error) {
          console.error(error);
        }
      }
      for (let record of this.records) {
        console.log(record);
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
          console.log("a", animalName);
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
        animal_name: animalName,
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
    async fetchAnimalName(animalId) {
      if (!animalId) {
        return null;
      }
      console.log("a", animalId);
      try {
        const response = await axios.get(`http://localhost:8000/animals/animal_name/${animalId}`);
        return response.data;
      } catch (error) {
        console.error("Error fetching animal:", error);
      }
    },
  },
};
</script>
