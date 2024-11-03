<template>
  <div class="bg-white shadow-md rounded-lg p-4 flex gap-4 mb-4">
    <div class="flex-1 pr-4">
      <p class="text-lg font-semibold text-gray-800">
        <router-link
          :to="`/animal/${reservation.borrow.animal.id}`"
          class="text-blue-500 hover:underline"
        >
          {{ reservation.borrow.animal.name }}
        </router-link>
        : Reservation from
        <router-link
          :to="`/volunteer/${reservation.volunteer.id}`"
          class="text-blue-500 hover:underline"
        >
          {{ reservation.volunteer.name }} {{ reservation.volunteer.surname }}
        </router-link>
      </p>
      <p class="text-sm text-gray-600">
        {{ formatDate(reservation.borrow.date) }} {{ formatTime(reservation.borrow.time) }}
      </p>
    </div>

    <div v-if="reservation.approved" class="flex-1/2 flex items-center space-x-4">
      <div class="flex items-center">
        <input
          type="checkbox"
          :checked="reservation.borrow.borrowed"
          @change="toggleBorrowed"
          id="borrowed-checkbox"
          class="mr-2"
        />
        <label for="borrowed-checkbox" class="text-gray-700">Borrowed</label>
      </div>
      <div class="flex items-center">
        <input
          type="checkbox"
          :checked="reservation.borrow.returned"
          @change="toggleReturned"
          id="returned-checkbox"
          class="mr-2"
        />
        <label for="returned-checkbox" class="text-gray-700">Returned</label>
      </div>
      <button
        @click="deleteReservation"
        class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600"
      >
        Delete
      </button>

    </div>

    <div v-if="!reservation.approved" class="flex-1/2 flex justify-end gap-2">
      <button
        @click="approveReservation"
        class="bg-green-500 text-white py-1 px-3 rounded-md hover:bg-green-600"
      >
        Approve
      </button>
      <button
        @click="deleteReservation"
        class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600"
      >
        Deny
      </button>

    </div>
  </div>
</template>

<script>

export default {
  props: {
    reservation: {
      type: Object,
      required: true,
    },
    isCaregiver: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    formatTime(time) {
      return time.slice(0, 5);
    },
    toggleBorrowed() {
      this.$emit('toggleBorrowed', this.reservation.id);
    },
    toggleReturned() {
      this.$emit('toggleReturned', this.reservation.id);
    },
    approveReservation() {
      this.$emit('approveReservation', this.reservation.id);
    },
    deleteReservation() {
      this.$emit('deleteReservation', this.reservation.id);
    },
  },
};
</script>

<style scoped>
/* Style adjustments for better readability */
</style>
