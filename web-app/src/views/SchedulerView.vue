<template>
  <div class="schedule-container h-screen">
    <NavigationBar />
    <div class="py-10">
      <div class="text-center font-bold mb-4">
        Selected Animal: {{ selectedAnimal ? selectedAnimal.name : 'Mr Mittens' }}
      </div>
      <div class="flex justify-between items-center mb-4">
        <button @click="previousWeek" class="p-2 bg-gray-300 rounded">&lt;</button>
        <div class="text-center font-bold">
          Week {{ currentWeek.week }}. {{ currentWeek.startDay }}.{{ currentWeek.startMonth }}. - {{ currentWeek.endDay }}.{{ currentWeek.endMonth }}. year {{ currentWeek.year }}
        </div>
        <button @click="nextWeek" class="p-2 bg-gray-300 rounded">&gt;</button>
      </div>
      <div class="grid grid-cols-14 gap-2">
        <div></div>
        <!-- Time headers on the top -->
        <div v-for="time in times" :key="time" class="text-center font-bold">{{ time }}</div>

        <!-- Days and corresponding time slots -->
        <div v-for="day in days" :key="day" class="contents">
          <!-- Day label on the first column -->
          <div class="text-right font-bold pr-2">{{ day }}</div>
          <!-- Time slots for that day -->
          <div v-for="time in times" :key="day + time"
               :class="getClass(getSlot(day, time))"
               @click="toggleSelection(day, time)"
               class="border p-2 cursor-pointer">
          </div>
        </div>
      </div>
      <button class="mt-4 p-2 bg-blue-500 text-white rounded" @click="confirmSelection">
        Confirm Reservation
      </button>
    </div>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';
import axios from 'axios';

export default {
  components: {
    NavigationBar
  },
  name: 'SchedulerView',
  data() {
    return {
      currentDate: new Date(),
      currentWeek: {},
      selectedAnimal: { name: 'Mr Mittens' }, // Hardcoded for now
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'],
      schedule: [],
      selected: []
    };
  },
  created() {
    this.currentWeek = this.getWeekDetails(this.currentDate);
    this.fetchSchedule(); // Fetch the schedule when component is created
  },
  methods: {
    getWeekDetails(date) {
      const currentDate = new Date(date);
      const startOfYear = new Date(currentDate.getFullYear(), 0, 1);
      const pastDaysOfYear = (currentDate - startOfYear) / 86400000;

      // Calculate the ISO week number
      const weekNumber = Math.ceil((pastDaysOfYear + startOfYear.getDay() + 1) / 7);

      // Calculate start and end dates of the week
      const startOfWeek = new Date(currentDate.setDate(currentDate.getDate() - currentDate.getDay() + 1));
      const endOfWeek = new Date(currentDate.setDate(startOfWeek.getDate() + 6));

      // Extract month and year
      const startMonth = startOfWeek.getMonth() + 1; // Months are zero-based
      const endMonth = endOfWeek.getMonth() + 1; // Months are zero-based
      const startDay = startOfWeek.getDate();
      const endDay = endOfWeek.getDate();
      const year = currentDate.getFullYear();

      return {
        week: weekNumber,
        startMonth: startMonth,
        endMonth: endMonth,
        startDay: startDay,
        endDay: endDay,
        year: year
      };
    },
    fetchSchedule() {
      const startDate = this.currentDate.toISOString().split('T')[0];
      // Fetch schedule from the backend API using axios
      const animalName = encodeURIComponent(this.selectedAnimal.name || 'Mr Mittens');
      axios.get(`/schedule/${animalName}/${startDate}`)
          .then(response => {
            this.schedule = response.data.schedule; // Update schedule with the data from the backend
          })
          .catch(error => {
            console.error('Error fetching schedule:', error);
          });
    },
    getSlot(day, time) {
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);
      return this.schedule[dayIndex] ? this.schedule[dayIndex][timeIndex] : 'gray';
    },
    getClass(slot) {
      if (slot === 'green') return 'bg-green-400';
      if (slot === 'red') return 'bg-red-400';
      if (slot === 'blue') return 'bg-blue-400';
      if (slot === 'selected') return 'bg-yellow-400';
      return 'bg-gray-200';
    },
    toggleSelection(day, time) {
      const slot = this.schedule[this.days.indexOf(day)][this.times.indexOf(time)];
      if (slot && slot === 'green') {
        this.schedule[this.days.indexOf(day)][this.times.indexOf(time)] = 'selected';
        this.selected.push({ day, time });
      } else if (slot && slot === 'selected') {
        this.schedule[this.days.indexOf(day)][this.times.indexOf(time)] = 'green';
        this.selected = this.selected.filter(s => s.day !== day || s.time !== time);
      }
    },
    confirmSelection() {
      this.$emit('reserveSlots', this.selected);
    },
    previousWeek() {
      this.currentDate.setDate(this.currentDate.getDate() - 7);
      this.currentWeek = this.getWeekDetails(this.currentDate);
      this.fetchSchedule(); // Fetch new week data
    },
    nextWeek() {
      this.currentDate.setDate(this.currentDate.getDate() + 7);
      this.currentWeek = this.getWeekDetails(this.currentDate);
      this.fetchSchedule(); // Fetch new week data
    }
  }
};
</script>

<style scoped>
.schedule-container {
  max-width: 900px;
  margin: 0 auto;
}

.grid-cols-14 {
  grid-template-columns: repeat(14, 1fr); /* One for days, 13 for time slots */
}

.border {
  border: 1px solid #ddd;
}

.cursor-pointer {
  cursor: pointer;
}
</style>
