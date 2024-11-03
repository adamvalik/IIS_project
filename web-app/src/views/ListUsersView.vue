<template>
  <div class="container mx-auto px-4 py-6">
    <NavigationBar />

    <div class="flex justify-between items-center mb-4">

      <h2 v-if="isAdmin" class="text-3xl font-bold text-gray-800 py-8">Manage Users</h2>
      <h2 v-else class="text-3xl font-bold text-gray-800 py-8">Manage Volunteers</h2>
      <button v-if="isAdmin" @click="openCreateUserModal" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">
        Add New User
      </button>
      <button v-else  @click="openCreateUserModal" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">
        Add New Volunteer
      </button>
    </div>

    <div v-if="loading" class="text-center">Loading...</div>
    <div v-if="!loading">
      <div class="grid grid-cols-1 gap-4">
        <UserRow
          v-for="user in users"
          :key="user.id"
          :user="user"
          :isAdmin="isAdmin"
          @editUser="openEditUserModal"
          @deleteUser="deleteUser"
          @verifyVolunteer="verifyVolunteer"
        />
      </div>
    </div>

    <UserModal
      v-if="showUserModal"
      :user="selectedUser"
      :isAdmin="isAdmin"
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
      showUserModal: false,
      selectedUser: null,
      isAdmin: false,
    };
  },
  async mounted() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.errorMessage = '';
      try {
        if (this.isAdmin) {
          const response = await axios.get("http://localhost:8000/users");
          this.users = response.data;
        } else {
          const response = await axios.get("http://localhost:8000/volunteers");
          this.users = response.data;
        }
      } catch (error) {
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
      this.selectedUser = { ...user };
      console.log(this.selectedUser);
      this.showUserModal = true;
    },
    async deleteUser(userId) {
      try {
        if (!userId) {
          console.error('No user ID provided');
          return;
        }
        await axios.delete(`http://localhost:8000/users/${userId}`);
        this.fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    async verifyVolunteer(userId) {
      try {
        if (!userId) {
          console.error('No user ID provided');
          return;
        }
        await axios.put(`http://localhost:8000/volunteers/${userId}/verify`);
        this.fetchUsers();
      } catch (error) {
        console.error('Error verifying volunteer:', error);
      }
    },
    closeUserModal() {
      this.showUserModal = false;
      this.fetchUsers();
    },
  },
};
</script>

<style scoped>
/* Additional styles can be added here */
</style>
