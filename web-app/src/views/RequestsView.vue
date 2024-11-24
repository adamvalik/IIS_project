<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 class="mb-4 text-3xl font-bold text-gray-800 py-8">Manage Examination Requests</h2>

    <h3 class="text-xl font-semibold text-gray-700 mb-4">Pending Requests</h3>
    <div v-if="pendingRequests.length" class="mb-8">
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
    <div v-else>
      <p class="text-gray-600 mb-4">No pending requests ✅</p>
    </div>

    <h3 class="text-xl font-semibold text-gray-700 mb-4">Processed Requests</h3>
    <div v-if="processedRequests.length">
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
    <div v-else>
      <p class="text-gray-600">No processed requests</p>
    </div>

    <WriteRecordModal
      v-if="showRecordModal"
      :show="showRecordModal"
      :request="selectedRequest"
      @close="closeRecordModal"
      @submitted="submitted"
    />

    <div v-if="showRecordSent" class="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg">
      Medical record submitted
    </div>

  </div>
</template>


<script>
import NavigationBar from '@/components/NavigationBar.vue';
import RequestRow from '@/components/RequestRow.vue';
import WriteRecordModal from '@/components/WriteRecordModal.vue';
import apiClient from '@/api';

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
      showRecordSent: false,
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
        const response = await apiClient.get("/requests");
        this.requests = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    writeMedicalRecord(id) {
      this.showRecordModal = true;
      this.selectedRequest = this.requests.find((request) => request.id === id);
    },
    submitted() {
      this.showRecordSent = true;
      setTimeout(() => {
        this.showRecordSent = false;
      }, 3000);
    },
    closeRecordModal() {
      this.showRecordModal = false;
      this.selectedRequest = null;
      this.fetchRequests();
    },
  },
};
</script>
