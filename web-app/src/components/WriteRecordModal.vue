<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-md p-6 w-full max-w-md">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Write Medical Record</h3>

      <!-- Display Current Date -->
      <p class="text-sm text-gray-600 mb-4">Date: {{ currentDate }}</p>

      <!-- Vaccination Type -->
      <div class="mb-4">
        <label for="vaccinationType" class="block text-sm font-medium text-gray-700">Vaccination Type (if applicable):</label>
        <input
          type="text"
          id="vaccinationType"
          v-model="formData.vaccinationType"
          placeholder="Enter vaccination type or leave empty"
          class="w-full border border-gray-300 rounded-md p-2 text-sm"
        />
      </div>

      <!-- Vet's Description -->
      <div class="mb-4">
        <label for="description" class="block text-sm font-medium text-gray-700">Description:</label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="4"
          placeholder="Enter examination details"
          class="w-full border border-gray-300 rounded-md p-2 text-sm"
        ></textarea>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-4">
        <button
          @click="$emit('close')"
          class="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-md"
        >
          Cancel
        </button>
        <button
          @click="submitRecord"
          class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md"
        >
          Submit
        </button>
      </div>
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
    },

    //   try {
    //     const payload = {
    //       vaccinationType: this.formData.vaccinationType || null,
    //       description: this.formData.description,
    //       date: this.currentDate,
    //       vetId: this.$store.getters.user_id, // Assuming vet ID is stored in Vuex
    //       requestId: this.request.id,
    //     };

    //     // Send data to the backend
    //     await axios.post("http://localhost:8000/medical_records", payload);

    //     alert("Medical record successfully submitted!");
    //     this.$emit("close");
    //   } catch (error) {
    //     console.error("Error submitting medical record:", error);
    //     alert("Failed to submit the medical record.");
    //   }
    // },
  },
};
</script>
