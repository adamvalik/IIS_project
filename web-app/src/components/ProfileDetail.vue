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
            <input type="text" v-model="user.name" class="w-full p-2 border border-gray-300 rounded-md text-sm" readonly />
          </div>

          <div>
            <label for="surname" class="block text-sm font-medium py-2">Surname:</label>
            <input type="text" v-model="user.surname" class="w-full p-2 border border-gray-300 rounded-md text-sm" readonly />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium py-2">Email:</label>
            <input type="email" v-model="user.email" class="w-full p-2 border border-gray-300 rounded-md text-sm" readonly />
          </div>

          <div>
            <label for="telephone" class="block text-sm font-medium py-2">Phone number:</label>
            <div class="flex gap-2">
              <input type="text" v-model="user.telephone" placeholder="Optional" class="w-3/4 p-2 border border-gray-300 rounded-md text-sm" />
              <input type="submit" value="Save" class="w-1/4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded" />
            </div>
          </div>

          <button @click="confirmDelete" type="button" class="mt-4 w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded">
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
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import NavigationBar from '@/components/NavigationBar.vue';

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
    };
  },
  computed: {
    ...mapGetters(['user_id']),

    userID() {
      return this.user_id;
    }
  },
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        console.log('Fetching profile...');
        console.log('User ID:', this.userID);
        const response = await axios.get(`http://localhost:8000/users/${this.userID}`);
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updatePhoneNum() {
      try {
        if (!this.user.telephone) {
          console.log('No phone number provided.');
          return;
        }
        await axios.put(`http://localhost:8000/users/${this.userID}/phone`, { phone: this.user.telephone });
        this.fetchProfile();
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    async changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert('Passwords do not match.');
        return;
      }
      try {
        await axios.post('/api/user/change-password', {
          currentPassword: this.currentPassword,
          newPassword: this.newPassword,
        });
      } catch (error) {
        console.error('Error changing password:', error);
      }
    },
    async deleteAccount() {
      try {
        await axios.delete('/api/user/delete-account');
      } catch (error) {
        console.error('Error deleting account:', error);
      }
      this.showDeleteDialog = false;
    },
  },
};
</script>
