<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-md p-6 w-full max-w-xl">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Medical Record</h3>

      <p class="text-sm text-gray-600 mb-4">Date: {{ currentDate }}</p>

      <!-- Vaccination Type -->
      <div class="mb-4">
        <label for="vaccinationType" class="block text-sm font-medium text-gray-800 mb-1">Vaccination Type (if applied):</label>
        <input
          type="text"
          id="vaccinationType"
          v-model="formData.vaccinationType"
          placeholder="Enter vaccination type or leave empty"
          class="w-full border border-gray-300 rounded-md p-2 text-sm"
        />
      </div>

      <!-- Weight -->
      <div class="mb-4 flex items-center gap-4">
        <label for="weight" class="block text-sm font-medium text-gray-800">Weight:</label>
        <input
          type="number"
          id="weight"
          v-model="formData.weight"
          class="w-16 border border-gray-300 rounded-md p-2 font-bold text-sm"
        />
        <p class="text-sm">kg</p>
      </div>

      <!-- Vet's Description -->
      <div class="mb-4">
        <label for="description" class="block text-sm font-medium text-gray-800 mb-1">Description:</label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="6"
          placeholder="Enter examination details"
          class="w-full border border-gray-300 rounded-md p-2 text-sm"
        ></textarea>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-between">
        <button
          @click="$emit('close')"
          class="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-md"
        >
          Cancel
        </button>
        <button
          @click="submitRecord"
          class="bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md"
        >
          Submit
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    request: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        vaccinationType: "",
        description: "",
        weight: null,
      },
      currentDate: new Date().toLocaleDateString(),
    };
  },
  methods: {
    async submitRecord() {
      if (!this.formData.description.trim()) {
        alert("Description is required.");
        return;
      }

      if (!this.formData.weight || this.formData.weight <= 0) {
        alert("Please enter a valid weight.");
        return;
      }

      try {
        const payload = {
          date: new Date().toISOString().split("T")[0],
          weight: this.formData.weight,
          vaccination: this.formData.vaccinationType == "" ? false : true,
          vaccination_type: this.formData.vaccinationType,
          vet_description: this.formData.description,
          id_animal: this.request.animal.id,
          id_veterinarian: this.$store.getters.user_id,
        };

        console.log("Medical record payload:", payload);

        await axios.post("http://localhost:8000/medical_records", payload);

        alert("Medical record successfully submitted!");
        this.$emit("close");
      } catch (error) {
        console.error("Error submitting medical record:", error);
        alert("Failed to submit the medical record.");
      }
    },
  },
};
</script>
