<template>
  <div class="flex justify-between items-center bg-white shadow p-4 rounded-lg">
    <div>
      <p class="text-lg font-semibold text-gray-700">{{ user.name }} {{ user.surname }}</p>
      <p class="text-sm text-gray-600">{{ user.email }}</p>
      <p class="text-sm text-gray-600">Role: {{ user.role }}</p>
    </div>
    <div class="flex gap-2">
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
    }
  },
  methods: {
    confirmDelete() {
      if (confirm(`Are you sure you want to delete ${this.user.name} ${this.user.surname}?`)) {
        this.$emit('deleteUser', this.user.id);
      }
    }
  }
};
</script>
