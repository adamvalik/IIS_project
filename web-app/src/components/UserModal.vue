<template>
  <div class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 w-full max-w-md">
      <h2 v-if="isAdmin" class="text-xl font-bold mb-4">{{ user ? "Edit User" : "Add New User" }}</h2>
      <h2 v-else class="text-xl font-bold mb-4">{{ user ? "Edit Volunteer" : "Add New Volunteer" }}</h2>
      <form @submit.prevent="saveUser">
        <div class="mb-4">
          <label class="block text-gray-700">Name</label>
          <input v-model="formData.name" type="text" class="w-full border rounded p-2" required>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Surname</label>
          <input v-model="formData.surname" type="text" class="w-full border rounded p-2" required>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Email</label>
          <input v-model="formData.email" type="email" class="w-full border rounded p-2" required>
        </div>
        <div v-if="isAdmin" class="mb-4">
          <label class="block text-gray-700">Role</label>
          <select v-model="formData.role" class="w-full border rounded p-2" required>
            <option value="volunteer">Volunteer</option>
            <option value="caregiver">Caregiver</option>
            <option value="veterinarian">Veterinarian</option>
          </select>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">{{ user ? "New Password" : "Password" }}</label>
          <input v-model="formData.password" type="password" class="w-full border rounded p-2" :required="!user">
        </div>

        <div class="flex justify-between">
          <button type="button" @click="$emit('close')" class="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600">
            Cancel
          </button>
          <button type="submit" class="bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600">
            {{ user ? "Update" : "Create" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  props: {
    user: {
      type: Object,
      default: null
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formData: {
        name: "",
        surname: "",
        email: "",
        role: "volunteer",
        password: null
      }
    };
  },
  watch: {
    user: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.formData = { ...newVal };
        } else {
          this.clearForm();
        }
      }
    }
  },
  mounted() {
    if (this.user) {
      this.formData = { ...this.user, password: null };
    }
  },
  methods: {
    async saveUser() {
      this.formData.name = this.formData.name.trim();
      this.formData.surname = this.formData.surname.trim();
      this.formData.email = this.formData.email.trim();

      try {
        if (!this.user) {
          const response = await apiClient.post("/email_validation", { email: this.formData.email });
          const email_in_use = response.data;
          if (email_in_use) {
            alert("Email already in use");
            this.formData.email = "";
            return;
          }
        }

        if (this.user) {
          // update existing user
          await apiClient.put(`/users/${this.user.id}`, this.formData);
        } else {
          // create new user
          await apiClient.post("/users", this.formData);
        }
        this.$emit("saveUser");
        this.$emit("close");
      } catch (error) {
        console.error("Error saving user:", error);
      }
    },
    clearForm() {
      this.formData = {
        name: "",
        surname: "",
        email: "",
        role: "volunteer",
        password: null
      };
    }
  }
};
</script>
