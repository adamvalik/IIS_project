<template>
  <div class="bg-white shadow-md rounded-lg p-4 flex gap-4 mb-4 relative">
    <div class="flex-1 pr-4">
      <p class="text-lg font-semibold text-gray-800">
        From
        <router-link
          :to="`/user/${request.caregiver.id}`"
          class="text-blue-500 hover:text-blue-600"
        >
          {{ request.caregiver.name }} {{ request.caregiver.surname }}
        </router-link>
          for
        <router-link
          :to="`/animal/${request.animal.id}`"
          class="text-blue-500 hover:text-blue-600"
        >
          {{ request.animal.name }}
        </router-link>
      </p>

      <p class="text-sm text-gray-600 max-w-3xl ">
        <span v-if="!showFullDescription">{{ truncatedDescription }}</span>
        <span v-else>{{ request.caregivers_description }}</span>
        <button v-if="showShowMore" @click="toggleDescription" class="text-blue-500 hover:underline ml-2">
          {{ showFullDescription ? "Show Less" : "Show More" }}
        </button>
      </p>
    </div>

    <div v-if="pending" class="flex" :class="showFullDescription ? 'absolute right-4 top-5' : 'items-center'">
      <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 font-semibold rounded-lg" @click="writeMedicalRecord">Write Medical Record</button>
    </div>
    <div v-else class="flex" :class="showFullDescription ? 'absolute right-4 top-4' : 'items-center'">
      <p class="text-sm text-gray-600 px-2 py-4">
        Processed by
        <router-link
          :to="`/user/${request.id_veterinarian}`"
          class="text-blue-500 hover:text-blue-600"
        >
          {{ veterinarian.name }} {{ veterinarian.surname }}
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  props: {
    request: {
      type: Object,
      required: true,
    },
    pending: {
      type: Boolean,
    },
  },
  data() {
    return {
      showFullDescription: false,
      showShowMore: false,
      veterinarian: {name: '', surname: ''},
      isAdmin: false,
    };
  },
  async mounted() {
    if (!this.pending) {
      try {
        const response = await apiClient.get(`/vet/${this.request.id_veterinarian}`);
        this.veterinarian = response.data;
      } catch (error) {
        console.error(error);
      }
    }
    this.isAdmin = this.$store.getters.userRole === 'admin';
  },
  computed: {
    truncatedDescription() {
      const maxLength = 100;
      const description = this.request.caregivers_description || '';
      if (description.length > maxLength) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.showShowMore = true;
        return description.slice(0, maxLength) + '...';
      } else {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.showShowMore = false;
        return description;
      }
    },
  },
  methods: {
    toggleDescription() {
      this.showFullDescription = !this.showFullDescription;
    },
    writeMedicalRecord() {
      if (this.isAdmin) {
        alert('Only veterinarians can write medical records.');
        return;
      }
      this.$emit('writeMedicalRecord', this.request.id);
    },
  },
};
</script>
