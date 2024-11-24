<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 class="mb-4 text-3xl font-bold text-gray-800 py-8">List Medical Records</h2>

    <h3 v-if="animal_id" class="text-xl font-semibold text-gray-700 mb-4">Medical Records for {{animal_name}}</h3>
    <h3 v-else class="text-xl font-semibold text-gray-700 mb-4">All Medical Records</h3>
<!--    The rows with the details of the medical records-->
    <div v-if="records.length">
      <div class="grid grid-cols-1 gap-3">
        <MedicalRecordRow
          v-for="record in records"
          :key="record.id"
          :showAnimalName="animal_id"
          :animal_name="record.animal_name"
          :record="record"
          :isAdmin="isAdmin"
          @toggleDetail="toggleDetail"
          @deleteRecord="deleteRecord"
          :class="{ 'mb-10': record.id === lastRecordId }"
        />
      </div>
    </div>
    <div v-else>
      <p v-if="animal_id" class="text-gray-700">No medical records for {{animal_name}} found.</p>
      <p v-else class="text-gray-700">No medical records found.</p>
    </div>
<!--    The selected record is shown below utilizing its data passed from the row-->
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
import NavigationBar from '@/components/NavigationBar.vue';
import MedicalRecordRow from "@/components/MedicalRecordRow.vue";
import RecordDetail from "@/components/RecordDetail.vue";
import apiClient from '@/api';

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
    // The data is fetched based on the route
    this.animal_id = this.$route.params.id;
    this.isCaregiver = this.$store.getters.userRole === 'caregiver' || this.$store.getters.userRole === 'admin';
    this.isVolunteer = this.$store.getters.userRole === 'volunteer';
    await this.fetchMedicalRecords();
    this.animal_name = await this.fetchAnimalName(this.animal_id);
  },
  computed: {
    lastRecordId() {
      return this.records.length ? this.records[this.records.length - 1].id : null;
    }
  },
  methods: {
    async fetchMedicalRecords() {
      if (!this.animal_id) {
        // Fetch all medical records if no animal_id is provided
        try {
          const response = await apiClient.get(`/all_medical_records`);
          this.records = response.data;
          for (let record of this.records) {
            record.animal_name = await this.fetchAnimalName(record.id_animal);
          }
        } catch (error) {
          console.error(error);
        }
      }
      else {
        // You looked to the records from the site of the animal
        try {
          const response = await apiClient.get(`/medical_records/${this.animal_id}`);
          this.records = response.data;
          for (let record of this.records) {
            record.animal_name = await this.fetchAnimalName(record.id_animal);
          }
        } catch (error) {
          console.error(error);
        }
      }

    },
    async toggleDetail(recordId) {
      // The details of the selected record are fetched
      let record = null;
      let veterinarianName = null;
      let animalName = null;

      try {
        const response = await apiClient.get(`/medical_record_get/${recordId}`);
        record = response.data;

      } catch (error) {
        console.error("Error fetching record details:", error);
      }
      if (record) {
        try{
          const response = await apiClient.get(`/vet/${record.id_veterinarian}`);
          veterinarianName = response.data.name + " " + response.data.surname;
        } catch (error) {
          console.error("Error fetching veterinarian:", error);
        }
        try{
          const response = await apiClient.get(`/animals/animal_name/${record.id_animal}`);
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
        animal_name: animalName,
        date: record.date,
        vaccination: vaccination_name,
        description: record.vet_description,
      };
      this.showModal = true;
    },
    deleteRecord(recordId) {
      if (confirm("Are you sure you want to delete this record?")) {
        apiClient.delete(`/medical_record_delete/${recordId}`)
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
      try {
        const response = await apiClient.get(`/animals/animal_name/${animalId}`);
        return response.data;
      } catch (error) {
        console.error("Error fetching animal:", error);
      }
    },
  },
};
</script>
