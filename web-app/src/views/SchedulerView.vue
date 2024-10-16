<template>
  <div class="schedule-container">
    <div class="flex justify-between items-center mb-4">
      <button @click="previousWeek" class="p-2 bg-gray-300 rounded">&lt;</button>
      <div class="text-center font-bold">
        Week {{ currentWeek.week }}.   {{ currentWeek.startDay }}.{{ currentWeek.startMonth }}. - {{ currentWeek.endDay }}.{{ currentWeek.endMonth }}.   year {{ currentWeek.year }}
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
</template>

<script>
export default {
  name: 'SchedulerView',
  data() {
    return {
      currentDate: new Date(),
      currentWeek: {},
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'],
      schedule: [
        { day: 'Mon', time: '09:00', status: 'green' },
        { day: 'Mon', time: '10:00', status: 'red' },
        { day: 'Tue', time: '09:00', status: 'blue' },
      ],
      selected: []
    };
  },
  created() {
    this.currentWeek = this.getWeekDetails(this.currentDate);
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
    getSlot(day, time) {
      return this.schedule.find(slot => slot.day === day && slot.time === time) || {status: 'gray'};
    },
    getClass(slot) {
      if (slot.status === 'green') return 'bg-green-400';
      if (slot.status === 'red') return 'bg-red-400';
      if (slot.status === 'blue') return 'bg-blue-400';
      if (slot.status === 'selected') return 'bg-yellow-400';
      return 'bg-gray-200';
    },
    toggleSelection(day, time) {
      const slot = this.schedule.find(s => s.day === day && s.time === time);
      if (slot && slot.status === 'green') {
        slot.status = 'selected';
        this.selected.push(slot);
      } else if (slot && slot.status === 'selected') {
        slot.status = 'green';
        this.selected = this.selected.filter(s => s !== slot);
      }
    },
    confirmSelection() {
      this.$emit('reserveSlots', this.selected);
    },
    previousWeek() {
      this.currentDate.setDate(this.currentDate.getDate() - 7);
      this.currentWeek = this.getWeekDetails(this.currentDate);
      // Fetch and update the schedule for the previous week
    },
    nextWeek() {
      this.currentDate.setDate(this.currentDate.getDate() + 7);
      this.currentWeek = this.getWeekDetails(this.currentDate);
      // Fetch and update the schedule for the next week
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