<template>
  <div class="container mx-auto px-4 py-10 max-w-lg">
    <div class="flex justify-center items-center mb-3">
      <router-link to="/" class="text-4xl font-bold text-gray-800">DJ Khaled's Animal Shelter</router-link>
    </div>

    <div class="bg-white shadow-lg rounded-lg p-8">
      <!-- <h2 class="text-2xl font-semibold text-gray-800 text-center">Sign Up</h2> -->
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label for="name" class="block text-gray-700 font-bold mb-2">Name <span class="text-red-500">*</span></label>
          <input
            v-model="name"
            type="text"
            id="name"
            placeholder="Enter your first name"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div class="mb-4">
          <label for="surname" class="block text-gray-700 font-bold mb-2">Surname <span class="text-red-500">*</span></label>
          <input
            v-model="surname"
            type="text"
            id="surname"
            placeholder="Enter your surname"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div class="mb-4">
          <label for="email" class="block text-gray-700 font-bold mb-2">Email <span class="text-red-500">*</span></label>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="Enter your email"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div class="mb-4">
          <label for="password" class="block text-gray-700 font-bold mb-2">Password <span class="text-red-500">*</span></label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Enter your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div class="mb-4">
          <label for="passwordConfirm" class="block text-gray-700 font-bold mb-2">Confirm Password <span class="text-red-500">*</span></label>
          <input
            v-model="passwordConfirm"
            type="password"
            id="passwordConfirm"
            placeholder="Confirm your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <p v-if="passwordsDoNotMatch" class="text-red-500 mt-2">Passwords do not match.</p>
        </div>

        <!-- telephone (optional) -->
        <div class="mb-6">
          <label for="telephone" class="block text-gray-700 font-bold mb-2">Telephone</label>
          <input
            v-model="telephone"
            type="tel"
            id="telephone"
            pattern="^[+]?[0-9]{0,3}\s?[0-9]{3}\s?[0-9]{3}\s?[0-9]{3}$"
            placeholder="Enter your telephone number"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-300"
        >
          Sign Up
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-700">
          Already have an account?
          <router-link to="/login" class="text-blue-500 hover:underline">Log In</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  name: 'SignUpPage',
  data() {
    return {
      name: '',
      surname: '',
      email: '',
      password: '',
      passwordConfirm: '',
      telephone: '',
    };
  },
  computed: {
    passwordsDoNotMatch() {
      return this.password !== this.passwordConfirm;
    }
  },
  methods: {
    async handleSubmit() {
      try {
        this.email = this.email.trim();
        const response = await apiClient.post("/email_validation", { email: this.email });
        const email_in_use = response.data;
        if (email_in_use) {
          alert("Email already in use");
          this.email = "";
          return;
        }
      } catch (error) {
        console.error("Error validating email:", error);
      }

      if (this.passwordsDoNotMatch) {
        alert("Passwords do not match.");
        return;
      }

      this.name = this.name.trim();
      this.surname = this.surname.trim();

      const newUser = {
        name: this.name,
        surname: this.surname,
        email: this.email,
        password: this.password,
        phone: this.telephone || null,
      };

      try {
        await apiClient.post('/signup', newUser);
        alert("Account created successfully, now please log in.");
        this.$router.push('/login');
      } catch (error) {
        alert("Sign up failed, reason: " + error.response.data.detail);
        this.$router.push('/');
      }
    },
  },
};
</script>

<style scoped>
input:focus {
  outline: none;
}

button[type="submit"] {
  font-size: 1.25rem;
}
</style>
