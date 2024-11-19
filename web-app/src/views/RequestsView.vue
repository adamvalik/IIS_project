<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 class="mb-4 text-3xl font-bold text-gray-800 py-8">Manage Examination Requests</h2>

    <div v-if="pendingRequests.length" class="mb-8">
      <h3 class="text-xl font-semibold text-gray-700 mb-4">Pending Requests</h3>
      <div class="grid grid-cols-1">
        <RequestRow
          v-for="request in pendingRequests"
          :key="request"
          :request="request"
          :pending="true"
          @writeMedicalRecord="writeMedicalRecord"
        />
      </div>
    </div>

    <div v-if="processedRequests.length">
      <h3 class="text-xl font-semibold text-gray-700 mb-4">Processed Requests</h3>
      <div class="grid grid-cols-1">
        <RequestRow
          v-for="request in processedRequests"
          :key="request"
          :request="request"
          :pending="false"
          @writeMedicalRecord="writeMedicalRecord"
        />
      </div>
    </div>

    <WriteRecordModal
      v-if="showRecordModal"
      :show="showRecordModal"
      :request="selectedRequest"
      @close="showRecordModal = false"
    />

  </div>
</template>


<script>
import axios from 'axios';
import NavigationBar from '@/components/NavigationBar.vue';
import RequestRow from '@/components/RequestRow.vue';
import WriteRecordModal from '@/components/WriteRecordModal.vue';

export default {
  components: {
    RequestRow,
    NavigationBar,
    WriteRecordModal,
  },
  data() {
    return {
      requests: [],
      showRecordModal: false,
      selectedRequest: null,
    };
  },
  computed: {
    pendingRequests() {
      return this.requests.filter((request) => request.id_veterinarian === null).sort((a, b) => a.id - b.id);
    },
    processedRequests() {
      return this.requests.filter((request) => request.id_veterinarian !== null).sort((a, b) => b.id - a.id);
    },
  },
  async mounted() {
    await this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      try {
        const response = await axios.get("http://localhost:8000/requests");
        this.requests = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    writeMedicalRecord(id) {
      // try {
      //   if (!id) {
      //     console.error('No reservation ID provided');
      //     return;
      //   }
      //   await axios.put(`http://localhost:8000/requests/${id}/processed/${this.$store.getters.user_id}`);
      //   this.fetchRequests();
      // } catch (error) {
      //   console.error('Error toggling returned:', error);
      // }
      this.showRecordModal = true;
      this.selectedRequest = this.requests.find((request) => request.id === id);
    },
  },
};
</script>
