<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <h2 v-if="isCaregiver" class="mb-4 text-3xl font-bold text-gray-800 py-8">Manage Reservations</h2>
    <h2 v-else-if="isVolunteer" class="mb-4 text-3xl font-bold text-gray-800 py-8">My Reservations</h2>

    <div v-if="futureReservations.length" class="mb-8">
      <h3 class="text-xl font-semibold text-gray-700 mb-4">Upcoming Reservations</h3>
      <div class="grid grid-cols-1">
        <ReservationRow
          v-for="reservation in futureReservations"
          :key="reservation.id"
          :reservation="reservation"
          :isCaregiver="isCaregiver"
          :isPast="false"
          @toggleBorrowed="toggleBorrowed"
          @toggleReturned="toggleReturned"
          @approveReservation="approveReservation"
          @deleteReservation="deleteReservation"
        />
      </div>
    </div>

    <div v-if="pastReservations.length">
      <h3 class="text-xl font-semibold text-gray-700 mb-4">Past Reservations</h3>
      <div class="grid grid-cols-1">
        <ReservationRow
          v-for="reservation in pastReservations"
          :key="reservation.id"
          :reservation="reservation"
          :isCaregiver="isCaregiver"
          :isPast="true"
          @toggleBorrowed="toggleBorrowed"
          @toggleReturned="toggleReturned"
          @approveReservation="approveReservation"
          @deleteReservation="deleteReservation"
        />
      </div>
    </div>

    <div v-if="!pastReservations.length && !futureReservations.length">
      <p class="text-gray-700">No reservations found.</p>
    </div>
  </div>
</template>


<script>
import NavigationBar from '@/components/NavigationBar.vue';
import ReservationRow from '@/components/ReservationRow.vue';
import apiClient from '@/api';

export default {
  components: {
    ReservationRow,
    NavigationBar,
  },
  data() {
    return {
      reservations: [],
      isCaregiver: false,
      isVolunteer: false,
    };
  },
  computed: {
    futureReservations() {
      const currentDate = new Date();
      return this.reservations.filter(
        reservation => new Date(reservation.borrow.date) >= currentDate
      );
    },
    pastReservations() {
      const currentDate = new Date();
      return this.reservations.filter(
        reservation => new Date(reservation.borrow.date) < currentDate
      );
    },
  },
  async mounted() {
    this.isCaregiver = this.$store.getters.userRole === 'caregiver' || this.$store.getters.userRole === 'admin';
    this.isVolunteer = this.$store.getters.userRole === 'volunteer';
    await this.fetchReservations();
  },
  methods: {
    async fetchReservations() {
      try {
        if (this.isCaregiver) {
          const response = await apiClient.get("/reservations");
          this.reservations = response.data;
        } else if (this.isVolunteer) {
          const response = await apiClient.get(`/reservations/volunteer/${this.$store.getters.user_id}`);
          this.reservations = response.data;
        }
      } catch (error) {
        console.error(error);
      }
    },
    async toggleBorrowed(reservationId) {
      try {
        if (!reservationId) {
          console.error('No reservation ID provided');
          return;
        }
        await apiClient.put(`/reservations/${reservationId}/toggle_borrowed`);
        this.fetchReservations();
      } catch (error) {
        console.error('Error toggling borrowed:', error);
      }
    },
    async toggleReturned(reservationId) {
      try {
        if (!reservationId) {
          console.error('No reservation ID provided');
          return;
        }
        await apiClient.put(`/reservations/${reservationId}/toggle_returned`);
        this.fetchReservations();
      } catch (error) {
        console.error('Error toggling returned:', error);
      }
    },
    async approveReservation(reservationId) {
      try {
        if (!reservationId) {
          console.error('No reservation ID provided');
          return;
        }
        await apiClient.put(`/reservations/${reservationId}/approve`);
        this.fetchReservations();
      } catch (error) {
        console.error('Error approving reservation:', error);
      }
    },
    async deleteReservation(reservationId) {
      try {
        if (!reservationId) {
          console.error('No reservation ID provided');
          return;
        }
        await apiClient.delete(`/reservations/${reservationId}`);
        this.fetchReservations();
      } catch (error) {
        console.error('Error deleting reservation:', error);
      }
    },
  },
};
</script>
