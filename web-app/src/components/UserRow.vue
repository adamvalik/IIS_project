<template>
  <div class="flex justify-between items-center bg-white shadow p-4 rounded-lg">
    <div>
      <router-link to="" class="text-lg font-semibold text-gray-700">{{ user.name }} {{ user.surname }}</router-link>
      <p class="text-sm text-gray-600">{{ user.email }}</p>
      <p class="text-sm text-gray-600">Role: {{ user.role }}</p>
      <p v-if="user.role === 'volunteer' && !isAdmin" class="text-sm text-gray-600">
        Verified:
        <span v-if="user.verified" class="text-green-500 font-semibold">Yes</span>
        <span v-else class="text-red-500 font-semibold">No</span>
      </p>
    </div>

    <div class="flex gap-2">
      <button v-if="!isAdmin && !user.verified && user.role === 'volunteer'" @click="verifyVolunteer" class="bg-green-500 text-white py-1 px-3 rounded-md hover:bg-green-600">
        Verify
      </button>
      <button @click="$emit('editUser', user)" class="bg-yellow-500 text-white py-1 px-3 rounded-md hover:bg-yellow-600">
        Edit
      </button>
      <button @click="confirmDelete" class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    confirmDelete() {
      if (confirm(`Are you sure you want to delete ${this.user.name} ${this.user.surname}?`)) {
        this.$emit('deleteUser', this.user.id);
      }
    },
    verifyVolunteer() {
      if (confirm(`Are you sure you want to verify ${this.user.name} ${this.user.surname}?`)) {
        this.$emit('verifyVolunteer', this.user.id);
      }
    }
  }
};
</script>
