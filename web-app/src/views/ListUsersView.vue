<template>
  <div class="container mx-auto px-4 py-6">
    <NavigationBar />

    <div class="flex justify-between items-center mb-4">
      <h2 class="text-3xl font-bold text-gray-800">Manage Users</h2>
      <button @click="openCreateUserModal" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">
        Add New User
      </button>
    </div>

    <!-- User List -->
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-if="errorMessage" class="text-center text-red-600">{{ errorMessage }}</div>

    <div v-if="!loading && !errorMessage">
      <div class="grid grid-cols-1 gap-4">
        <UserRow
          v-for="user in users"
          :key="user.id"
          :user="user"
          @editUser="openEditUserModal"
          @deleteUser="deleteUser"
        />
      </div>
    </div>

    <!-- User Modal (for creating/editing users) -->
    <UserModal
      v-if="showUserModal"
      :user="selectedUser"
      @close="closeUserModal"
      @saveUser="fetchUsers"
    />
  </div>
</template>

<script>
import axios from 'axios';
import UserRow from '@/components/UserRow.vue';
import UserModal from '@/components/UserModal.vue';
import NavigationBar from '@/components/NavigationBar.vue';

export default {
  components: {
    UserRow,
    UserModal,
    NavigationBar,
  },
  data() {
    return {
      users: [],
      loading: true,
      errorMessage: '',
      showUserModal: false,
      selectedUser: null, // User object for editing, or null for creating a new user
    };
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.errorMessage = '';
      try {
        const response = await axios.get("http://localhost:8000/users");
        this.users = response.data;
      } catch (error) {
        this.errorMessage = 'Failed to load users.';
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    openCreateUserModal() {
      this.selectedUser = null;
      this.showUserModal = true;
    },
    openEditUserModal(user) {
      this.selectedUser = { ...user }; // Pass a copy to avoid direct editing
      this.showUserModal = true;
    },
    async deleteUser(userId) {
      try {
        await axios.delete(`${process.env.VUE_APP_BACKEND_URL}/users/${userId}`);
        this.fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    closeUserModal() {
      this.showUserModal = false;
      this.fetchUsers();
    },
  },
  async mounted() {
    await this.fetchUsers();
  },
};
</script>

<style scoped>
/* Additional styles can be added here */
</style>
