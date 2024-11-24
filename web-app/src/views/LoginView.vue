<template>
  <div class="container mx-auto px-4 py-10 max-w-lg h-screen flex flex-col justify-center">
    <router-link to="/" class="text-4xl font-bold text-gray-800 text-center mb-10">DJ Khaled's Animal Shelter</router-link>

    <div class="bg-white shadow-lg rounded-lg p-8">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-6">Login</h2>
      <form @submit.prevent="handleSubmit">
        <div class="mb-6">
          <label for="email" class="block text-gray-700 font-bold mb-2">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="Enter your email"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div class="mb-6 relative">
          <label for="password" class="block text-gray-700 font-bold mb-2">Password</label>
          <input
            :type="passwordFieldType"
            v-model="password"
            id="password"
            placeholder="Enter your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="absolute inset-y-0 right-3 top-7 flex items-center text-gray-500 text-xl"
          >
            <span v-if="passwordFieldType === 'password'">
              👀
            </span>
            <span v-else>
              🤫
            </span>
          </button>
        </div>

        <button
          type="submit"
          class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-300"
        >
          Log In
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-700">
          Don’t have an account?
          <router-link to="/signup" class="text-blue-500 hover:underline">Sign Up</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';
export default {
  data() {
    return {
      email: '',
      password: '',
      passwordFieldType: 'password',
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
    handleSubmit() {

      apiClient.post('/login', {
        email: this.email,
        password: this.password
      })
      .then(response => {
        this.$store.dispatch('login', response.data.access_token);
        this.$router.push('/');
      })
      .catch(error => {
        alert("Login failed, reason: " + error.response.data.detail);
        this.password = '';
      });
    }
  }
};
</script>

<style scoped>
input:focus {
  outline: none;
}

input[type="email"],
input[type="password"] {
  font-size: 1rem;
}

button[type="submit"] {
  font-size: 1.25rem;
}
</style>
