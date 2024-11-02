<!-- AnimalTile.vue -->
<template>
  <div class="bg-white shadow-md rounded-lg p-6 hover:shadow-xl transition-all">
    <!-- Animal Image -->
    <img :src="photo" :alt="name" class="w-full h-48 object-cover rounded-md mb-4" />

    <!-- Animal Information -->
    <h3 class="text-xl font-semibold text-gray-700">{{ name }}</h3>
    <p class="text-gray-500 mt-2">{{ species }}</p>
    <p class="text-gray-500">Age: {{ calculateAge(birth_year) }} years</p>

    <!-- Optional Slot for Action Buttons or Extra Information -->
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "AnimalTile",
  props: {
    name: {
      type: String,
      required: true
    },
    species: {
      type: String,
      required: true
    },
    birth_year: {
      type: Number,
      required: true
    },
    photo: {
      type: String,
      required: false
    }
  },
  methods: {
    calculateAge(birthYear) {
        const currentYear = new Date().getFullYear();
        return currentYear - birthYear;
      }
  }
};
</script>
