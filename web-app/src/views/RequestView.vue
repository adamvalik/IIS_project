<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 v-if="isCaregiver" class="mb-4 text-3xl font-bold text-gray-800 py-8">Manage requests</h2>

    <div class="grid grid-cols-1">
      <ReservationRow
        v-for="request in requests"
        :key="reservation.id"
        :reservation="reservation"
        :isCaregiver="isCaregiver"
        @toggleBorrowed="toggleBorrowed"
        @toggleReturned="toggleReturned"
        @approveReservation="approveReservation"
        @deleteReservation="deleteReservation"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavigationBar from '@/components/NavigationBar.vue';
import ReservationRow from '@/components/ReservationRow.vue';

export default {
  components: {
    ReservationRow,
    NavigationBar,
  },
  data() {
    return {
      requests: [],
      selectedReservation: null,
      isVeterinarian: false,
    };
  },
  async mounted() {
    this.isVeterinarian = this.$store.getters.userRole === 'veterinarian';
    await this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      this.errorMessage = '';
      try {
        if (this.isVeterinarian) {
          const response = await axios.get("http://localhost:8000/reservations");
          this.requests = response.data;
        }
      } catch (error) {
        console.error(error);
      }
    },
    // async toggleBorrowed(reservationId) {
    //   try {
    //     if (!reservationId) {
    //       console.error('No reservation ID provided');
    //       return;
    //     }
    //     await axios.put(`http://localhost:8000/reservations/${reservationId}/toggle_borrowed`);
    //     this.fetchReservations();
    //   } catch (error) {
    //     console.error('Error toggling borrowed:', error);
    //   }
    // },
    // async toggleReturned(reservationId) {
    //   try {
    //     if (!reservationId) {
    //       console.error('No reservation ID provided');
    //       return;
    //     }
    //     await axios.put(`http://localhost:8000/reservations/${reservationId}/toggle_returned`);
    //     this.fetchReservations();
    //   } catch (error) {
    //     console.error('Error toggling returned:', error);
    //   }
    // },
    // async approveReservation(reservationId) {
    //   try {
    //     if (!reservationId) {
    //       console.error('No reservation ID provided');
    //       return;
    //     }
    //     await axios.put(`http://localhost:8000/reservations/${reservationId}/approve`);
    //     this.fetchReservations();
    //   } catch (error) {
    //     console.error('Error approving reservation:', error);
    //   }
    // },
    // async deleteReservation(reservationId) {
    //   try {
    //     if (!reservationId) {
    //       console.error('No reservation ID provided');
    //       return;
    //     }
    //     await axios.delete(`http://localhost:8000/reservations/${reservationId}`);
    //     this.fetchReservations();
    //   } catch (error) {
    //     console.error('Error deleting reservation:', error);
    //   }
    // },
  },
};
</script>
