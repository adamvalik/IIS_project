<template>
  <div class="container mx-auto py-6 px-4 h-screen">
    <NavigationBar />
    <div class="flex mx-auto flex-col lg:flex-row w-full lg:w-3/4 gap-8 mt-6 bg-white shadow-md rounded-lg p-6">
      <!-- Left Column: User Information and Password Change -->
      <div class="w-full lg:w-1/2 space-y-6">
        <h2 class="text-2xl font-semibold">My Profile</h2>

        <form @submit.prevent="updateProfile" class="">
          <div>
            <label for="name" class="block text-sm font-medium py-2">Name:</label>
            <input type="text" v-model="user.name" class="input-field" readonly />
          </div>

          <div>
            <label for="surname" class="block text-sm font-medium py-2">Surname:</label>
            <input type="text" v-model="user.surname" class="input-field" readonly />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium py-2">Email:</label>
            <input type="email" v-model="user.email" class="input-field" readonly />
          </div>

          <div>
            <label for="telephone" class="block text-sm font-medium py-2">Telephone:</label>
            <input type="text" v-model="user.telephone" placeholder="Optional" class="input-field" />
          </div>

          <!-- Delete Account Button -->
          <button @click="confirmDelete" type="button" class="mt-4 w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded">
            Delete Account
          </button>

          <!-- Delete Confirmation Dialog -->
          <div v-if="showDeleteDialog" class="mt-4 p-4 bg-gray-100 border border-gray-300 rounded-lg">
            <p>Are you sure you want to delete your account?</p>
            <div class="flex gap-4 mt-2">
              <button @click="deleteAccount" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Yes</button>
              <button @click="showDeleteDialog = false" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">No</button>
            </div>
          </div>
        </form>
      </div>

      <!-- Right Column: Account Status and Actions -->
      <div class="w-full lg:w-1/2 space-y-6">
        <h3 class="text-xl font-semibold">Account Status</h3>

        <!-- Approval Checkbox (Read-only) -->
        <label class="flex items-center text-lg space-x-2">
          <input type="checkbox" :checked="user.isApproved" disabled class="form-checkbox" />
          <span>Approved</span>
        </label>

        <!-- Authorization Level Button (Visible only if Admin) -->
        <button v-if="isAdmin" @click="authorizeUser" class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 rounded">
          Approve Authorization Level
        </button>

        <!-- Change Password Section -->
        <div class="password-change space-y-4">
          <h3 class="text-xl font-semibold">Change Password</h3>

          <div>
            <label for="currentPassword" class="block text-sm font-medium">Current Password:</label>
            <input type="password" v-model="currentPassword" class="input-field" />
          </div>

          <div>
            <label for="newPassword" class="block text-sm font-medium">New Password:</label>
            <input type="password" v-model="newPassword" class="input-field" />
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium">Confirm New Password:</label>
            <input type="password" v-model="confirmPassword" class="input-field" />
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
import NavigationBar from '@/components/NavigationBar.vue';

export default {
  components: {
    NavigationBar,
  },
  name: 'UserProfile',
  data() {
    return {
      user: {
        name: '',
        surname: '',
        email: '',
        telephone: '',
        isApproved: false,
      },
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      showDeleteDialog: false,
      isAdmin: false,
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('/api/user/profile');
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updateProfile() {
      try {
        await axios.put('/api/user/profile', { telephone: this.user.telephone });
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
    async authorizeUser() {
      alert('Authorization level change requested.');
    },
    confirmDelete() {
      this.showDeleteDialog = true;
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
  created() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
.input-field {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}
</style>

