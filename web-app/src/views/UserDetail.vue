<template>
  <div class="container mx-auto px-4 py-6 min-h-scree">
    <NavigationBar class="mb-4" />

    <div class="max-w-4xl mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      <div class="p-8 space-y-6">
        <h1 class="text-2xl font-semibold text-gray-800">User Details</h1>

        <div class="flex flex-col gap-6 md:flex-row items-center md:items-start md:gap-10">
          <!-- Placeholder Avatar -->
          <div class="flex-shrink-0">
            <div class="h-32 w-32 rounded-full overflow-hidden bg-gray-100 shadow-md">
              <div
                class="h-full w-full flex items-center justify-center bg-gradient-to-br from-gray-200 to-gray-300 text-gray-500"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-16 w-16 text-gray-400"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12 2a6 6 0 100 12 6 6 0 000-12zM4 20.25a8.25 8.25 0 1116.5 0v.25a.75.75 0 01-.75.75h-15a.75.75 0 01-.75-.75v-.25z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </div>
          </div>


          <div class="flex flex-col gap-3">
            <div>
              <p class="font-semibold text-gray-700">Name</p>
              <p class="text-lg text-gray-600">{{ user.name }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-700">Surname</p>
              <p class="text-lg text-gray-600">{{ user.surname }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-700">E-mail</p>
              <p class="text-lg text-gray-600">{{ user.mail }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-700">Phone number</p>
              <p class="text-lg text-gray-600">{{ user.telephone }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-700">Role</p>
              <p class="text-lg text-gray-600 capitalize">{{ user.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavigationBar from '../components/NavigationBar.vue';
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      user: {},
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole', 'user_id']),

    isCaregiver() {
      return this.userRole === 'caregiver';
    },
  },
  async mounted() {
    const userID = this.$route.params.id;
    this.fetchUser(userID);
  },
  methods: {
    async fetchUser(id) {
      try {
        const response = await axios.post('http://localhost:8000/user_detail', {
          id: id,
        });
        this.user = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
