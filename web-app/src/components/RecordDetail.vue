<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50" @click.self="closeModal">
    <div class="bg-white rounded-lg shadow-md p-6 w-full max-w-xl">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Medical Record Details</h3>
      <div class="grid grid-cols-2 gap-2">
        <p class="text-lg text-gray-600">Animal Name:</p>
        <p class="text-lg text-gray-600">{{ animalName }}</p>
        <p class="text-lg text-gray-600">Veterinarian:</p>
        <p class="text-lg text-gray-600">{{ veterinarianName }}</p>
        <p class="text-lg text-gray-600">Date:</p>
        <p class="text-lg text-gray-600">{{ date }}</p>
        <p v-if="vaccination" class="text-lg text-gray-600">Vaccination:</p>
        <p v-if="vaccination" class="text-lg text-gray-600">{{ vaccination }}</p>
        <p class="text-lg text-gray-600 col-span-2">Description:</p>
        <textarea rows="6" class="w-full border border-gray-300 rounded-md p-2 col-span-2" v-model="localDescription" disabled></textarea>
      </div>
      <button @click="closeModal" class="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg font-semibold mt-4">Close</button>
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
  data() {
    return {
      localDescription: this.description,
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>
