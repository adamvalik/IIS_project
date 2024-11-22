<template>
  <div class="bg-white shadow-md rounded-lg p-6 hover:shadow-xl transition-all">
    <img :src="photo" :alt="name" class="w-full h-48 object-cover rounded-md mb-4" />

    <h3 class="text-xl font-semibold text-gray-700">{{ name }}</h3>
    <p class="text-gray-500 mt-2">{{ species }}</p>
    <p class="text-gray-500">{{ showAge() }}</p>
  </div>
</template>

<script>
export default {
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
      required: true
    }
  },
  methods: {
    showAge() {
      if (!this.birth_year) {
        return "Age: Unknown";
      } else if (this.calculateAge(this.birth_year) === 0) {
        return 'Age: Less than a year';
      } else if (this.calculateAge(this.birth_year) === 1) {
        return 'Age: ' + this.calculateAge(this.birth_year) + ' year';
      } else {
        return 'Age: ' + this.calculateAge(this.birth_year) + ' years';
      }
    },
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear();
      return currentYear - birthYear;
    }
  }
};
</script>
