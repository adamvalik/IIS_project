<template>
  <div class="flex justify-between items-center bg-white shadow p-4 rounded-lg">
    <div>
      <p class="text-lg font-semibold text-gray-700">{{ record.date }}</p>
      <p v-if="!showAnimal" class="text-sm text-gray-600">Animal: {{ animal_name }}</p>
      <p class="text-sm text-gray-600">Veterinarian: {{ veterinarian }}</p>
    </div>

    <div class="flex gap-2">
      <button @click="toggleDetail" class="bg-yellow-500 text-white py-1 px-3 rounded-md hover:bg-yellow-600">
        Show Details
      </button>
      <button v-if="isAdmin" @click="deleteRecord" class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600">
        Delete
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
    showAnimalName: {
      type: Number,
      required: false
    },
    animal_name: {
      type: String,
      required: true
    },
    isAdmin: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      veterinarian : null,
      showAnimal : null
    };
  },
  created() {
    this.fetchVeterinarianName();
    this.showAnimal = this.showAnimalName;
    console.log("skrrrrrrr", this.showAnimal);
  },
  methods: {
    toggleDetail() {
      console.log("det", this.record.id);
      this.$emit('toggleDetail', this.record.id);
    },
    async fetchVeterinarianName() {
      try {
        console.log(this.record.id_veterinarian);
        const response = await axios.get(`http://localhost:8000/vet/${this.record.id_veterinarian}`);
        this.veterinarian = response.data.name + " " + response.data.surname;
      } catch (error) {
        console.error(error);
      }
    },
    deleteRecord() {
      this.$emit('deleteRecord', this.record.id);
    }
  }
};
</script>
