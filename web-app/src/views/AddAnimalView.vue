<template>
  <div class="container mx-auto py-6 px-4">
    <NavigationBar />

    <h2 class="text-2xl font-semibold my-6 text-center">Add New Animal</h2>

    <form @submit.prevent="addAnimal" class="bg-white shadow-md rounded-lg p-6 space-y-4 max-w-lg mx-auto">
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
          max="2024"
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
        <label for="admission_date" class="block text-sm font-medium text-gray-700">Admission Date:</label>
        <input
          type="date"
          v-model="formData.admission_date"
          id="admission_date"
          class="w-full p-2 border border-gray-300 rounded-md text-sm"
        />
      </div>

      <div class="w-full">
        <label for="photo" class="block text-sm font-medium text-gray-700">Photo:</label>
        <div class="flex items-center gap-4 mt-2">
          <label
            for="photo"
            class="bg-blue-500 text-white text-sm font-bold py-2 px-4 rounded-md cursor-pointer hover:bg-blue-600"
          >
            Select File
          </label>
          <span v-if="selectedFileName" class="text-gray-600">{{ selectedFileName }}</span>
          <span v-else class="text-gray-500">No file selected</span>
        </div>
        <!-- hidden default file input design -->
        <input
          type="file"
          @change="handleFileUpload"
          id="photo"
          class="hidden"
        />
      </div>

      <input
        type="submit"
        class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-md"
        value="Add Animal"
      />
    </form>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';
import apiClient from '@/api';

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      formData: {
        name: '',
        species: '',
        breed: null,
        birth_year: null,
        size: null,
        caregivers_description: null,
        admission_date: this.getTodayDate(),
        photo: null,
      },
      selectedFileName: null,
    };
  },
  methods: {
    getTodayDate() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    async handleFileUpload(event) {
      const file = event.target.files[0];
      // validate file type
      const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg'];
      if (!file || !validFileTypes.includes(file.type)) {
        alert('Please upload a valid image file (JPEG, PNG, or GIF)');
        return;
      }
      // MEDIUMBLOB limit (16 MB)
      const maxSize = 16 * 1024 * 1024;
      if (file.size > maxSize) {
        alert("File size exceeds 16 MB. Please upload a smaller image.");
        return;
      }

      this.selectedFileName = file.name;

      // convert file to bytes
      const reader = new FileReader();
      reader.onload = () => {
        this.formData.photo = reader.result.split(',')[1]; // get base64 part
      };
      reader.readAsDataURL(file);
    },
    async addAnimal() {
      try {
        const payload = {
          name: this.formData.name,
          species: this.formData.species,
          breed: this.formData.breed,
          birth_year: this.formData.birth_year,
          photo: this.formData.photo,
          admission_date: this.formData.admission_date,
          size: this.formData.size,
          caregivers_description: this.formData.caregivers_description,
          id_caregiver: this.$store.getters.user_id,
        };
        console.log('Adding animal:', payload);
        await apiClient.post('/animals', payload);
        alert('Animal added successfully');
        this.resetForm();
      } catch (error) {
        alert('Failed to add animal: ' + error.message);
        console.error('Error adding animal:', error);
      }
    },
    resetForm() {
      this.formData = {
        name: '',
        species: '',
        breed: null,
        birth_year: null,
        size: null,
        caregivers_description: null,
        admission_date: this.getTodayDate(),
        photo: null,
        selectedFileName: null,
      };
    },
  },
};
</script>
