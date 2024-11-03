<template>
  <div class="container mx-auto px-4 py-6">
    <NavigationBar />

    <h2 v-if="isCaregiver" class="mb-4 text-3xl font-bold text-gray-800 py-8">Manage Reservations</h2>
    <h2 v-else-if="isVolunteer" class="mb-4 text-3xl font-bold text-gray-800 py-8">My Reservations</h2>
    <h2 v-else class="mb-4 text-3xl font-bold text-gray-800 py-8" style="display:none;">Manage Users or Volunteers</h2>

    <div v-if="loading" class="text-center">Loading...</div>
    <div v-if="!loading">
      <div class="grid grid-cols-1 gap-4">
        <ReservationRow
          v-for="reservation in reservations"
          :key="reservation.id"
          :reservation="reservation"
          :isCaregiver="isCaregiver"
          @deleteReservation="deleteReservation"
        />
      </div>
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
      reservations: [],
      loading: true,
      selectedReservation: null,
      isCaregiver: false,
      isVolunteer: false,
    };
  },
  async mounted() {
    this.isCaregiver = this.$store.getters.userRole === 'caregiver' || this.$store.getters.userRole === 'admin';
    this.isVolunteer = this.$store.getters.userRole === 'volunteer';
    await this.fetchReservations();
  },
  methods: {
    async fetchReservations() {
      this.loading = true;
      this.errorMessage = '';
      try {
        if (this.isCaregiver) {
          const response = await axios.get("http://localhost:8000/reservations");
          this.reservations = response.data;
        } else if (this.isVolunteer) {
          const response = await axios.get(`http://localhost:8000/reservations/volunteer/{this.$store.getters.user_id}`);
          this.reservations = response.data;
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    // async deleteReservation(userId) {
    //   try {
    //     if (!userId) {
    //       console.error('No user ID provided');
    //       return;
    //     }
    //     await axios.delete(`http://localhost:8000/users/${userId}`);
    //     this.fetchUsers();
    //   } catch (error) {
    //     console.error('Error deleting user:', error);
    //   }
    // },
    // async verifyVolunteer(userId) {
    //   try {
    //     if (!userId) {
    //       console.error('No user ID provided');
    //       return;
    //     }
    //     await axios.put(`http://localhost:8000/volunteers/${userId}/verify`);
    //     this.fetchUsers();
    //   } catch (error) {
    //     console.error('Error verifying volunteer:', error);
    //   }
    // },
  },
};
</script>
