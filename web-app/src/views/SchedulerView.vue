<template>

  <div class="schedule-container h-screen relative" @click="showPopup=false">

    <NavigationBar />

    <div class="py-10">

      <div class="text-center font-bold mb-4">
        Selected Animal: {{ selectedAnimal ? selectedAnimal.name : 'Bella' }}
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
        <div v-for="time in times" :key="time" class="text-center font-bold">{{ time }}</div>
        <div v-for="day in days" :key="day" class="contents">
          <div class="text-right font-bold pr-2">{{ day }}</div>
          <div v-for="time in times" :key="day + time"
               :class="getClass(getSlot(day, time))"
               @click.stop ="toggleSelection(day, time)"
               class="border p-2 cursor-pointer relative">
          </div>
        </div>
      </div>

      <button class="mt-4 p-2 bg-blue-500 text-white rounded" @click="confirmSelection">
        Confirm Reservation
      </button>

      <button v-if="getRole === 'caregiver'" class="mt-4 p-2 bg-green-500 text-white rounded" @click="createNewSlot">
        Create New Slot
      </button>

      <!-- Pop-up Window -->
      <div v-if="showPopup.visible" class="popup absolute bg-white border p-4 rounded shadow-lg" style="top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 50;" @click.stop>
        <p class="font-bold">Waiting for approval</p>
        <p>Name: Satek</p>
        <p>Time: {{ showPopup.time }}</p>
        <p>Date: {{ showPopup.date }}</p>
        <button @click="cancelReservation" class="mt-2 px-3 py-1 bg-red-500 text-white rounded">Cancel Reservation</button>
        <p class="text-sm text-gray-600 mt-2">If you are canceling less than 24 hours before the appointment, please call us at +69696969</p>
      </div>

    </div>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole', 'tokenExp', 'user_id']),
    getID() {
      return this.user_id;
    },
    getRole() {
      return this.userRole;
    }
  },
  components: {
    NavigationBar
  },
  name: 'SchedulerView',
  data() {
    return {
      currentDate: new Date(),
      currentWeek: {},
      selectedAnimal: {name: 'Bella'}, // Hardcoded for now
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'],
      schedule: [],
      selected: [],
      new_slots: [],
      hoveredSlot: {day: null, time: null}, // Initialize hoveredSlot with default values
      showPopup: { visible: false, day: '', time: '', date: '' } // Control the visibility of the popup and store day, time, date
    };
  },
  created() {
    console.log('User ID:', this.getID);
    console.log('User Role:', this.getRole);
    this.currentWeek = this.getWeekDetails(this.currentDate);
    this.fetchSchedule(); // Fetch the schedule when component is created
  },
  methods: {
    getWeekDetails(date) {
      const currentDate = new Date(date);
      const dayOfWeek = currentDate.getDay(); // Get the current day of the week (0-6)
      const startOfWeek = new Date(currentDate);
      startOfWeek.setDate(currentDate.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1)); // Adjust to Monday (start of the week)

      const endOfWeek = new Date(startOfWeek);
      endOfWeek.setDate(startOfWeek.getDate() + 6); // Calculate the end of the week

      // Extract month and year
      const startMonth = startOfWeek.getMonth() + 1; // Months are zero-based
      const endMonth = endOfWeek.getMonth() + 1; // Months are zero-based
      const startDay = startOfWeek.getDate();
      const endDay = endOfWeek.getDate();
      const year = currentDate.getFullYear();

      return {
        week: Math.ceil((currentDate - new Date(currentDate.getFullYear(), 0, 1)) / 604800000) + 1, // Calculate ISO week number
        startMonth: startMonth,
        endMonth: endMonth,
        startDay: startDay,
        endDay: endDay,
        year: year
      };
    },
    fetchSchedule() {
      const startOfWeek = new Date(this.currentDate.setDate(this.currentDate.getDate() - this.currentDate.getDay() + 1));
      const startDate = startOfWeek.toISOString().split('T')[0];
      const animal_id = 1;
      const user_id = this.getID;

      axios.post('http://localhost:8000/schedule', {
        user_id: user_id,
        animal_id: animal_id,
        date: startDate
      })
        .then(response => {
          const scheduleData = response.data.schedule;
          this.schedule = Array.from({ length: 7 }, (_, day) =>
            Array.from({ length: 13 }, (_, hour) =>
              scheduleData[day]?.[hour + 9] || "blue" // Map backend data to array format
            )
          );
        })
        .catch(error => {
          console.error('Error fetching schedule:', error);
        });
    },
    getSlot(day, time) {
      const dayIndex = this.days.indexOf(day);
      const timeIndex = parseInt(time.split(':')[0]) - 9; // convert time string (e.g., "09:00") to an hour offset

      if (
          dayIndex >= 0 && dayIndex < 7 &&
          this.schedule[dayIndex] &&
          this.schedule[dayIndex][timeIndex] !== undefined
      ) {
        return this.schedule[dayIndex][timeIndex];
      }
      return 'gray';
    },
    getClass(slot) {
      if (slot === 'green') return 'bg-green-400';
      if (slot === 'red') return 'bg-red-400';
      if (slot === 'blue') return 'bg-blue-400';
      if (slot === 'orange') return 'bg-orange-400';
      if (slot === 'pink') return 'bg-pink-400';
      if (slot === 'selected') return 'bg-yellow-400';
      return 'bg-gray-200';
    },
    toggleSelection(day, time) {
      const slotStatus = this.getSlot(day, time);
      if (slotStatus === 'green' || slotStatus === 'orange') {
        const dayIndex = this.days.indexOf(day);
        const startOfWeek = new Date(this.currentDate);
        startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1); // Set to the start of the week
        const selectedDate = new Date(startOfWeek);
        selectedDate.setDate(startOfWeek.getDate() + dayIndex);
        const formattedDate = selectedDate.toISOString().split('T')[0];

        this.showPopup = { visible: true, day, time, date: formattedDate };
      } else {
        if (this.showPopup.visible) {
          this.showPopup.visible = false;
        }
      }

      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      if (dayIndex >= 0 && timeIndex >= 0) {
        const slot = this.schedule[dayIndex][timeIndex];
        if (slot === 'blue' && this.getRole !== 'caregiver') {
          this.schedule[dayIndex][timeIndex] = 'selected';
          this.selected.push({day, time});
        } else if (slot === 'selected') {
          this.schedule[dayIndex][timeIndex] = 'blue';
          this.selected = this.selected.filter(s => !(s.day === day && s.time === time));
        } else if (slot === 'blue' && this.getRole === 'caregiver') {
          this.deleteSlot(day, time);
        } else if (slot === 'gray' && this.getRole === 'caregiver') {
          this.new_slots.push({day, time});
          this.schedule[dayIndex][timeIndex] = 'pink';
        }
      }
    },
    createNewSlot() {
      const startOfWeek = new Date(this.currentDate);
      startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1); // Set to the start of the week
      const newSlots = this.new_slots.map(slot => {
        const dayIndex = this.days.indexOf(slot.day);
        const selectedDate = new Date(startOfWeek);
        selectedDate.setDate(startOfWeek.getDate() + dayIndex);
        const formattedDate = selectedDate.toISOString().split('T')[0];
        return { day: slot.day, time: slot.time, date: formattedDate };
      });

      axios.post('http://localhost:8000/createslot', {
        animal_id: 1,
        new_slots: newSlots
      })
        .then(response => {
          console.log('Slot created:', response.data);
          newSlots.forEach(slot => {
            const dayIndex = this.days.indexOf(slot.day);
            const timeIndex = this.times.indexOf(slot.time);
            this.schedule[dayIndex][timeIndex] = 'blue';
          });
          this.new_slots = []; // Clear the new slots
        })
        .catch(error => {
          console.error('Error creating slot:', error);
        });
    },
    confirmSelection() {
      const startOfWeek = new Date(this.currentDate);
      startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1); // Set to the start of the week
      const selectedSlots = this.selected.map(slot => {
        const dayIndex = this.days.indexOf(slot.day);
        const selectedDate = new Date(startOfWeek);
        selectedDate.setDate(startOfWeek.getDate() + dayIndex);
        const formattedDate = selectedDate.toISOString().split('T')[0];
        return { day: slot.day, time: slot.time, date: formattedDate };
      });
      const user_id = this.getID;
      axios.post('http://localhost:8000/confirmselection', {
        user_id: user_id,
        animal_id: 1,
        slots: selectedSlots
      })
          .then(response => {
            console.log('Reservation confirmed:', response.data);
            // Make the slots orange to indicate pending confirmation
            selectedSlots.forEach(slot => {
              const dayIndex = this.days.indexOf(slot.day);
              const timeIndex = this.times.indexOf(slot.time);
              this.schedule[dayIndex][timeIndex] = 'orange';
            });
            this.selected = []; // Clear the selected slots
          })
          .catch(error => {
            console.error('Error confirming reservation:', error);
          });
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
    },
    cancelReservation() {
      const { day, time, date } = this.showPopup;
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      if (dayIndex >= 0 && timeIndex >= 0) {
        this.schedule[dayIndex][timeIndex] = 'blue';
        this.selected = this.selected.filter(s => !(s.day === day && s.time === time));
        this.showPopup.visible = false;

        const animalId = 1;
        const userId = this.getID;
        axios.delete(`http://localhost:8000/cancel/${userId}/${animalId}/${date}/${time}`)
            .then(response => {
              console.log('Reservation canceled:', response.data);
            })
            .catch(error => {
              console.error('Error canceling reservation:', error);
            });
      }
    },
    deleteSlot(day, time) {
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      const startOfWeek = new Date(this.currentDate);
      startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1); // Set to the start of the week
      const selectedDate = new Date(startOfWeek);
      selectedDate.setDate(startOfWeek.getDate() + dayIndex);
      const formattedDate = selectedDate.toISOString().split('T')[0];

      if (dayIndex >= 0 && timeIndex >= 0) {

        const animalId = 1;
        axios.delete(`http://localhost:8000/delete/${animalId}/${formattedDate}/${time}`)
          .then(response => {
            console.log('Slot Deleted:', response.data);
            this.new_slots = this.new_slots.filter(s => !(s.day === day && s.time === time));
            this.schedule[dayIndex][timeIndex] = 'gray';
          })
          .catch(error => {
            console.error('Error deleting slot:', error);
          });
      }
    },
    showInfo(day, time) {
      this.hoveredSlot = {day, time};
    },
    hideInfo() {
      this.hoveredSlot = {day: null, time: null};
    },
    confirmInfo() {
      console.log('confirm');
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

.info-table {
  top: 0;
  left: 100%;
  z-index: 10;
  width: 150px;
  transform: translateX(10px); /* Adjust the position to be next to the cell */
}
</style>
