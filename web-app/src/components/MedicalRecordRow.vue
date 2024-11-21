<template>
  <div class="flex justify-between items-center bg-white shadow p-4 rounded-lg">
    <div>
      <p class="text-lg font-semibold text-gray-700">{{ record.date }}</p>
      <p v-if="!showAnimal" class="text-sm text-gray-600">
        Animal:
        <router-link
          :to="`/animal/${record.id_animal}`"
          class="text-blue-500 hover:text-blue-600"
        >
          {{ animal_name }}
        </router-link>
      </p>
      <p class="text-sm text-gray-600">
        Veterinarian:
        <router-link
          :to="`/user/${record.id_veterinarian}`"
          class="text-blue-500 hover:text-blue-600"
        >
          {{ veterinarian }}
        </router-link>
      </p>
    </div>

    <div class="flex gap-2">
      <button @click="toggleDetail" class="bg-yellow-500 text-white py-2 px-4 rounded-lg font-semibold hover:bg-yellow-600">
        Show Details
      </button>
      <button v-if="isAdmin" @click="deleteRecord" class="bg-red-500 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-600">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';

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
  },
  methods: {
    toggleDetail() {
      this.$emit('toggleDetail', this.record.id);
    },
    async fetchVeterinarianName() {
      try {
        const response = await apiClient.get(`/vet/${this.record.id_veterinarian}`);
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
