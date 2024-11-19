<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50" @click.self="closeModal">
    <div class="bg-white rounded-lg shadow-md p-6 w-full max-w-xl">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Medical Record Details</h3>
      <p class="text-sm text-gray-600 mb-2">Animal Name: {{ animalName }}</p>
      <p class="text-sm text-gray-600 mb-2">Veterinarian: {{ veterinarianName }}</p>
      <p class="text-sm text-gray-600 mb-2">Date: {{ date }}</p>
      <p v-if="vaccination" class="text-sm text-gray-600 mb-2">Vaccination: {{ vaccination }}</p>
      <p class="text-sm text-gray-600 mb-4">Description: {{ description }}</p>
      <button @click="closeModal" class="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-md">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    animalName: {
      type: String,
      required: true,
    },
    veterinarianName: {
      type: String,
      required: true,
    },
    date: {
      type: String,
      required: true,
    },
    vaccination: {
      type: String,
      default: null,
    },
    description: {
      type: String,
      required: true,
    },
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>
