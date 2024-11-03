<template>
  <div class="bg-white shadow-md rounded-lg p-4 flex justify-between items-center">
    <div>
      <h3 class="text-lg font-semibold text-gray-800">Reservation ID: {{ reservation.id }}</h3>
      <p class="text-sm text-gray-600">Approved: {{ reservation.approved ? 'Yes' : 'No' }}</p>
      <p class="text-sm text-gray-600">Volunteer: {{ reservation.volunteer.name }} {{ reservation.volunteer.surname }}</p>
      <p class="text-sm text-gray-600">Borrow Date: {{ formatDate(reservation.borrow.date) }}</p>
      <p class="text-sm text-gray-600">Borrow Time: {{ formatTime(reservation.borrow.time) }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    reservation: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    formatTime(time) {
      return new Date(`1970-01-01T${time}Z`).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>
