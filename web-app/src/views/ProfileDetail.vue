<template>
  <div class="container mx-auto py-6 px-4 h-screen">
    <NavigationBar />
    <div class="flex mx-auto flex-col lg:flex-row w-full lg:w-3/4 gap-8 mt-6 bg-white shadow-md rounded-lg p-6">
      <!-- left column -->
      <div class="w-full lg:w-1/2 space-y-6">
        <h2 class="text-2xl font-semibold">My Profile</h2>

        <form @submit.prevent="updatePhoneNum">
          <div>
            <label for="name" class="block text-sm font-medium py-2">Name:</label>
            <input type="text" name="name" id="name" v-model="user.name" class="w-full p-2 border border-gray-300 rounded-md text-sm" disabled/>
          </div>

          <div>
            <label for="surname" class="block text-sm font-medium py-2">Surname:</label>
            <input type="text" name="surname" id="surname" v-model="user.surname" class="w-full p-2 border border-gray-300 rounded-md text-sm" disabled />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium py-2">Email:</label>
            <input type="email" name="email" id="email" v-model="user.email" class="w-full p-2 border border-gray-300 rounded-md text-sm" disabled />
          </div>

          <div>
            <label for="phone" class="block text-sm font-medium py-2">Phone number:</label>
            <div class="flex gap-2">
              <input
                v-model="user.phone"
                type="tel"
                id="phone"
                name="phone"
                pattern="^[+]?[0-9]{0,3}\s?[0-9]{3}\s?[0-9]{3}\s?[0-9]{3}$"
                placeholder="Enter your phone number"
                class="w-3/4 p-2 border border-gray-300 rounded-md text-sm"
                required
              />
              <input type="submit" value="Save" class="w-1/4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded" />
            </div>
          </div>

          <button v-if="!isAdmin" @click="deleteAccount" type="button" class="mt-4 w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded">
            Delete Account
          </button>
        </form>
      </div>

      <!-- right column -->
      <div class="w-full lg:w-1/2 flex flex-col justify-between">
        <div v-if="user.role === 'volunteer'">
          <p class="text-xl font-semibold">Account Status</p>
          <p v-if="user.verified" class="text-green-500 font-semibold">Verified</p>
          <p v-else class="text-red-500 font-semibold">Not Verified</p>
        </div>
        <div v-else>
          <p class="text-xl font-semibold">Role</p>
          <p class="font-semibold text-blue-500">{{ user.role }}</p>
        </div>

        <div class="space-y-4">
          <h3 class="text-xl font-semibold">Change Password</h3>

          <div>
            <label for="currentPassword" class="block text-sm font-medium">Current Password:</label>
            <input type="password" v-model="currentPassword" class="w-full p-2 border border-gray-300 rounded-md text-sm" />
          </div>

          <div>
            <label for="newPassword" class="block text-sm font-medium">New Password:</label>
            <input type="password" v-model="newPassword" class="w-full p-2 border border-gray-300 rounded-md text-sm" />
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium">Confirm New Password:</label>
            <input type="password" v-model="confirmPassword" class="w-full p-2 border border-gray-300 rounded-md text-sm" />
          </div>

          <button @click="changePassword" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded">
            Confirm Password Change
          </button>
        </div>
      </div>
    </div>

    <div v-if="showPhoneUpdated" class="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg">
      Phone number updated
    </div>
    <div v-if="showPwdUpdated" class="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg">
      Password changed successfully
    </div>
  </div>
</template>

<script>
// import axios from 'axios';
import { mapGetters } from 'vuex';
import NavigationBar from '@/components/NavigationBar.vue';
import apiClient from '@/api';

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      user: {
        type: Object,
        default: null
      },
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      showPhoneUpdated: false,
      showPwdUpdated: false,
    };
  },
  computed: {
    ...mapGetters(['user_id']),

    userID() {
      return this.user_id;
    },
    isAdmin() {
      return this.user.role === 'admin';
    }
  },
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await apiClient.get(`/users/${this.userID}`);
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updatePhoneNum() {
      try {
        await apiClient.put(`/users/${this.userID}/phone`, { phone: this.user.phone });
        this.fetchProfile();
        this.showPhoneUpdated = true;
        setTimeout(() => {
          this.showPhoneUpdated = false;
        }, 3000);
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    async changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert('Passwords do not match.');
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        return;
      }
      if (this.newPassword === '' || this.confirmPassword === '') {
        alert('Please enter a new password with 1 or more characters.');
        return;
      }
      try {
        await apiClient.put(`/users/${this.userID}/password`, {
          oldPassword: this.currentPassword,
          newPassword: this.newPassword,
        });
        this.showPwdUpdated = true;
        setTimeout(() => {
          this.showPwdUpdated = false;
        }, 3000);
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
      } catch (error) {
        alert('Error changing password. Please check your current password.');
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';

      }
    },
    async deleteAccount() {
      try {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
          await apiClient.delete(`/users/${this.userID}`);
          this.$store.dispatch('logout');
          this.$router.push('/');
        }
      } catch (error) {
        console.error('Error deleting account:', error);
      }
    },
  },
};
</script>
