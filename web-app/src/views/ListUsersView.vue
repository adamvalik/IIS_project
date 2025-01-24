<template>
  <div class="container mx-auto px-4 py-6 h-screen">
    <NavigationBar />

    <div class="flex justify-between items-center mb-4">

      <h2 v-if="isAdmin" class="text-3xl font-bold text-gray-800 py-8">Manage Users</h2>
      <h2 v-else-if="isCaregiver" class="text-3xl font-bold text-gray-800 py-8">Manage Volunteers</h2>
      <h2 v-else class="text-3xl font-bold text-gray-800 py-8" style="display:none;">Manage Users or Volunteers</h2>

      <button v-if="isAdmin" @click="openCreateUserModal" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg">
        Add New User
      </button>
      <button v-else  @click="openCreateUserModal" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg">
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
          :class="{ 'mb-10': user.id === lastUserId }"
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
import UserRow from '@/components/UserRow.vue';
import UserModal from '@/components/UserModal.vue';
import NavigationBar from '@/components/NavigationBar.vue';
import apiClient from '@/api';

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
      isCaregiver: false,
    };
  },
  computed: {
    lastUserId() {
      return this.users.length ? this.users[this.users.length - 1].id : null;
    }
  },
  async mounted() {
    this.isAdmin = this.$store.getters.userRole === 'admin';
    this.isCaregiver = this.$store.getters.userRole === 'caregiver';
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.errorMessage = '';
      try {
        if (this.isAdmin) {
          const response = await apiClient.get("/users");
          this.users = response.data;
        } else {
          const response = await apiClient.get("/volunteers");
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
      this.showUserModal = true;
    },
    async deleteUser(userId) {
      try {
        if (!userId) {
          console.error('No user ID provided');
          return;
        }
        await apiClient.delete(`/users/${userId}`);
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
        await apiClient.put(`/volunteers/${userId}/verify`);
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
