<template>
  <div class="flex justify-between items-center bg-white shadow p-4 rounded-lg">
    <div>
      <p class="text-lg font-semibold text-gray-700">{{ record.date }}</p>
      <p class="text-sm text-gray-600">Veterinarian: {{ veterinarian }}</p>
    </div>

    <div class="flex gap-2">
      <button @click="$emit('toggleDetail', record.id)" class="bg-yellow-500 text-white py-1 px-3 rounded-md hover:bg-yellow-600">
        Show Details
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    record: {
      type: Object,
      required: true
    },
    animal_name: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      veterinarian : null
    };
  },
  created() {
    this.fetchVeterinarianName();
  },
  methods: {
    toggleDetail() {
      if (confirm(`Are you sure you want to delete ${this.user.name} ${this.user.surname}?`)) {
        this.$emit('deleteUser', this.user.id);
      }
    },
    async fetchVeterinarianName() {
      try {
        console.log(this.record.veterinarian_id);
        const response = await axios.get(`http://localhost:8000/vet/${this.record.id_veterinarian}`);
        this.veterinarian = response.data.name + " " + response.data.surname;
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>
