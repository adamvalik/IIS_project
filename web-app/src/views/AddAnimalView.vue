<template>
  <div class="container mx-auto py-6 px-4 h-screen">
    <NavigationBar />

    <h2 class="text-2xl font-semibold mb-6">Add New Animal</h2>

    <form @submit.prevent="addAnimal" class="bg-white shadow-md rounded-lg p-6 space-y-4">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700">Name:</label>
        <input
          type="text"
          v-model="formData.name"
          id="name"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
          required
        />
      </div>

      <div>
        <label for="species" class="block text-sm font-medium text-gray-700">Species:</label>
        <input
          type="text"
          v-model="formData.species"
          id="species"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
          required
        />
      </div>

      <div>
        <label for="breed" class="block text-sm font-medium text-gray-700">Breed:</label>
        <input
          type="text"
          v-model="formData.breed"
          id="breed"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
        />
      </div>

      <div>
        <label for="birth_year" class="block text-sm font-medium text-gray-700">Birth Year:</label>
        <input
          type="number"
          v-model="formData.birth_year"
          id="birth_year"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
          min="1900"
          max="2100"
        />
      </div>

      <div>
        <label for="size" class="block text-sm font-medium text-gray-700">Size:</label>
        <select
          v-model="formData.size"
          id="size"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
        >
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-gray-700">Caregiver's Description:</label>
        <textarea
          v-model="formData.caregivers_description"
          id="description"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
        ></textarea>
      </div>

      <div>
        <label for="photo" class="block text-sm font-medium text-gray-700">Photo:</label>
        <input
          type="file"
          @change="handleFileUpload"
          id="photo"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
        />
      </div>

      <button
        type="submit"
        class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-md"
      >
        Add Animal
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import NavigationBar from '@/components/NavigationBar.vue';

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      formData: {
        name: '',
        species: '',
        breed: '',
        birth_year: null,
        size: '',
        caregivers_description: '',
        photo: null,
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.formData.photo = file;
    },
    async addAnimal() {
      try {
        const formData = new FormData();
        formData.append('name', this.formData.name);
        formData.append('species', this.formData.species);
        formData.append('breed', this.formData.breed || '');
        formData.append('birth_year', this.formData.birth_year);
        formData.append('size', this.formData.size);
        formData.append('caregivers_description', this.formData.caregivers_description);

        if (this.formData.photo) {
          formData.append('photo', this.formData.photo);
        }

        await axios.post('http://localhost:8000/animals', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // Clear the form after submission
        this.resetForm();
        alert('Animal added successfully!');
      } catch (error) {
        console.error('Error adding animal:', error);
        alert('Failed to add animal. Please try again.');
      }
    },
    resetForm() {
      this.formData = {
        name: '',
        species: '',
        breed: '',
        birth_year: null,
        size: '',
        caregivers_description: '',
        photo: null,
      };
    },
  },
};
</script>
